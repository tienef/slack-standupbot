import locale
from standup.model.conversation import Conversation
from standup.model.report import Report
from datetime import datetime
import html


# Localisation en FR
locale.setlocale(locale.LC_ALL, 'fra_fra')


class StandUpBot:
    def __init__(self, slackClient, confluenceClient, spaceKey, conflMainContentName, slackChannel, conflServer):
        self.slack = slackClient
        self.confluence = confluenceClient
        self.spaceKey = spaceKey
        self.conflMainContentName = conflMainContentName
        self.slackChannel = slackChannel
        self.conflServer = conflServer

    def run(self):
        allConversations = []
        allReports = []

        # Récupération de l'id du channel
        channelsList = self.slack.get("/api/channels.list",
                       {'token': self.slack.token})
        for channel in channelsList["channels"]:
            if channel["name"] == self.slackChannel:
                channelId = channel["id"]
        if not channelId:
            return("Aucun channel Slack de ce nom n'existe !")

        # Récupération des messages pour chaque utilisateur (=conversation) sur le channel demandé de ce jour
        now = datetime.now()
        nowTS = int(now.timestamp())
        dayStartTS = int(datetime(now.year, now.month, now.day).timestamp())
        MessagesList = self.slack.get("/api/channels.history",
                                      {'token': self.slack.token, 'channel': channelId,
                                       'latest': nowTS, 'oldest': dayStartTS, 'count' : "1000"})

        for message in MessagesList["messages"]:
            found = False
            for elemen in allConversations:
                if elemen.user_id == message["user"]:
                    elemen.messages.append(message["text"])
                    found = True
            if not found:
                conversation = Conversation()
                conversation.user_id = message["user"]
                conversation.messages.append(message["text"])
                allConversations.append(conversation)

        # Pour chaque conversation, on regarde si elle contient un message déclenchant la génération d'un rapport
        for conversation in allConversations:
            for message in conversation.messages:
                if ((message[:5].lower() == "today") or (message[:9].lower() in ("yesterday", "obstacles"))):
                    conversation.startsReport = True

        # Pour chaque conversation devant déclencher un rapport, on construit le rapport.
        for conversation in allConversations:
            if conversation.startsReport:
                report = Report()
                for message in conversation.messages:
                    if (message[:5].lower() == "today") and (report.today == ''):
                        report.today = message[6:]
                    if (message[:9].lower() == "yesterday") and (report.yesterday == ''):
                        report.yesterday = message[10:]
                    if (message[:9].lower() == "obstacles") and (report.obstacles == ''):
                        report.obstacles = message[10:]
                # On récupère le nom de l'utilisateur pour chaque rapport
                slackUserInfoResponse = self.slack.get("/api/users.info",
                                                       {'token': self.slack.token, 'user': conversation.user_id})
                report.name = slackUserInfoResponse['user']['real_name']
                allReports.append(report)

        # On définie le titre du rapport d'après la date du jour
        title = "Stand-up report : " + now.strftime("%a %d %B %Y")

        # On récupère le contentId et le numéro de version de la page existante. S'il en existe pas ou qu'il y en a plusieurs, on récupère False
        conflContent = self.confluence.get_contentId_from_title(title, self.spaceKey)

        # On constitue le HTML
        HTML = '<html xmlns:string=\"xalan://java.lang.String\" xmlns:lxslt=\"http://xml.apache.org/xslt\"><head><title>%(title)s</title></head><body>' % {
            'title': title}
        for report in allReports:
            HTML += '<h2>%(user)s</h2><table class=\"details\" border=\"0\" cellpadding=\"5\" cellspacing=\"2\" width=\"95%%\"><tr valign=\"top\" class=\"TableRowColor\"><th>Yesterday</th><td width=\"90%%\">%(yesterday)s</td></tr><tr valign=\"top\" class=\"TableRowColor\"><th>Today</th><td>%(today)s</td></tr><tr valign=\"top\" class=\"TableRowColor\"><th>Obstacles</th><td>%(obstacles)s</td></tr></table>' \
                    % {'user': html.escape(report.name, quote=True),
                       'yesterday': html.escape(report.yesterday, quote=True),
                       'today': html.escape(report.today, quote=True),
                       'obstacles': html.escape(report.obstacles, quote=True)}
        HTML += "</body></html>"

        # On récupère le conflMainContentId à partir du conflMainContentName
        conflMainContent = self.confluence.get_contentId_from_title(self.conflMainContentName, self.spaceKey)
        conflMainContentId = conflMainContent["contentId"]

        # Page déjà existante : on l'écrase
        if conflContent:
            conflContentId = conflContent["contentId"]
            #On récupère le numéro de version de la page existante
            conflGetContentIdResponse = self.confluence.get_content("/rest/api/content/%s" % conflContentId, {})
            conflContentVersion = int(conflGetContentIdResponse["version"]["number"])
            # On constitue le JSON contenant le HTML
            JSON = {"type": "page",
                    "title": "%s" % title,
                    "ancestors": [{'id': conflMainContentId}],
                    "space": {'key': self.spaceKey},
                    "version": {'number' : conflContentVersion+1},
                    "body": {'storage': {'value': HTML, 'representation': 'storage'}}}
            conflContentCreationResponse = self.confluence.update_content("/rest/api/content/%s" % conflContentId, JSON)

        # Page non existante : on la créé
        else:
            # On constitue le JSON contenant le HTML
            JSON = {"type": "page",
                    "title": "%s" % title,
                    "ancestors": [{'id': conflMainContentId}],
                    "space": {'key': self.spaceKey},
                    "version": {'number' : '1'},
                    "body": {'storage': {'value': HTML, 'representation': 'storage'}}}
            conflContentCreationResponse = self.confluence.create_content("/rest/api/content", JSON)
            # On modifie le purpose du channel Slack
            self.slack.get("/api/channels.setPurpose", {'token': self.slack.token, 'channel': channelId,
                                                        'purpose': self.conflServer +
                                                                   conflContentCreationResponse["_links"]["webui"]})
        return("Rapport traité sans erreur")