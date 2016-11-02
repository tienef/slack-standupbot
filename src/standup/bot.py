import locale
from standup.model.conversation import Conversation
from datetime import datetime

#Localisation en FR
locale.setlocale(locale.LC_ALL, 'fra_fra')

class StandUpBot:

    def __init__(self, slackClient, confluenceClient):
        self.slack = slackClient
        self.confluence = confluenceClient

    def run(self):
        allConversations = []
        allReports = []

        #Récupération des conversactions directe entre le bot et les users
        slackIMListResponse = self.slack.get("/api/im.list", {"token" : self.slack.token})

        #Pour chaque im engagé avec le bot, on instancie un nouveau rapport
        for im in slackIMListResponse['ims']:
            conversation = Conversation()
            conversation.user_id = im['user']
            conversation.id = im['id']
            allConversations.append(conversation)

        #Pour chaque conversation, on récupère la liste des messages de ce jour
        now = datetime.now()
        nowTS = int(now.timestamp())
        dayStartTS = int(datetime(now.year, now.month, now.day).timestamp())
        for conversation in allConversations:
            slackIMHistoryResponse = self.slack.get("/api/im.history", {'token' : self.slack.token, 'channel' : conversation.id, 'latest' : nowTS, 'oldest' : dayStartTS })
            for message in slackIMHistoryResponse['messages']:
                conversation.messages.append(message['text'])

        #Pour chaque conversation, on regarde si elle contient un message déclenchant la génération d'un rapport
        for conversation in allConversations:
            for message in conversation.messages:
                if ((message[:5].lower() == "today") or (message[:9].lower() in ("yesterday", "obstacles"))):
                    conversation.startsReport = True

        #Pour chaque conversation devant déclencher un rapport, on construit le rapport.
        for conversation in allConversations:
            if conversation.startsReport == True:
                report = Report()
                for message in conversation.messages:
                    if (message[:5].lower() == "today") and (report.today == ''):
                        report.today = message[5:]
                    if (message[:9].lower() == "yesterday") and (report.yesterday == ''):
                        report.yesterday = message[9:]
                    if (message[:9].lower() == "obstacles") and (report.obstacles == ''):
                        report.obstacles = message[9:]
                ##On récupère le nom de l'utilisateur pour chaque rapport
                slackUserInfoResponse = self.slack.get("/api/users.info", {'token' : self.slack.token, 'user' : conversation.user_id})
                report.name = slackUserInfoResponseJSON['user']['real_name']
                allReports.append(report)

        #On regarde s'il existe déjà une page confluence