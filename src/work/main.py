import urllib.request
import json
from datetime import datetime

"""
##Localisation en FR
locale.setlocale(locale.LC_ALL, 'fra_fra')

##Slack
slackToken = "xoxb-89846243653-IAcQ287gmTpCB9xKcVkl1iKo"
slackServer = "https://slack.com"

##Confluence
conflServer = "https://docs.kepler-rominfo.com"
conflContentId = "24740688"
conflUser = "thomas.faivre"
conflPassword = "thomas.faivre"

class Conversation:
    def __init__(self):
        self.id = ''
        self.user_id = ''
        self.messages = []
        self.startsReport = False

class Report:
    def __init__(self):
        self.yesterday = ''
        self.today = ''
        self.obstacles = ''
        self.user_id = ''
        self.name = ''
"""
allConversations = []
allReports = []

##Récupération des conversactions directe entre le bot et les users
slackIMListRequest = urllib.request.Request(url='https://slack.com/api/im.list?token=%s' % slackToken, method='GET')
slackIMListResponse = urllib.request.urlopen(slackIMListRequest)
slackIMListResponseJSON = json.loads(slackIMListResponse.read().decode('utf-8'))

##Pour chaque im engagé avec le bot, on instancie un nouveau Report

for im in slackIMListResponseJSON['ims']:
    conversation = Conversation()
    conversation.user_id = im['user']
    conversation.id = im['id']
    allConversations.append(conversation)

##Pour chaque conversation, on récupère la liste des messages de ce jour
now = datetime.now()
nowTS = int(now.timestamp())
dayStartTS = int(datetime(now.year, now.month,now.day).timestamp())
for conversation in allConversations:
    slackIMHistoryRequest = urllib.request.Request(url='https://slack.com/api/im.history?token=%(token)s&channel=%(channel)s&latest=%(latest)s&oldest=%(oldest)s&inclusive=1' % {'token' : slackToken, 'channel' : conversation.id, 'latest' : nowTS, 'oldest' : dayStartTS }, method='GET')
    slackIMHistoryResponse = urllib.request.urlopen(slackIMHistoryRequest)
    slackIMHistoryResponseJSON = json.loads(slackIMHistoryResponse.read().decode('utf-8'))
    for message in slackIMHistoryResponseJSON['messages']:
        conversation.messages.append(message['text'])

##Pour chaque conversation, on regarde si elle contient un message déclenchant la génération d'un rapport
for conversation in allConversations:
    for message in conversation.messages:
        if ((message[:5].lower() == "today") or (message[:9].lower() in ("yesterday", "obstacles"))):
            conversation.startsReport = True

##Pour chaque conversation devant déclencher un rapport, on construit le rapport.
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
        slackUserInfoRequest = urllib.request.Request(
            url='https://slack.com/api/users.info?token=%(token)s&user=%(user)s' % {
                'token': slackToken, 'user': conversation.user_id}, method='GET')
        slackUserInfoResponseJSON = json.loads(urllib.request.urlopen(slackUserInfoRequest).read().decode('utf-8'))
        report.name = slackUserInfoResponseJSON['user']['real_name']
        allReports.append(report)

##On regarde si la version en cours sur Confluence
title = "Stand-up report : " + now.strftime("%a %d %B %Y")
print(title)

conflGetContentRequest = urllib.request.Request(
            url=conflServer + '/rest/api/content?title=%(title)s' % {
                'title': title}, method='GET')
conflGetContentResponse = urllib.request.urlopen(conflGetContentRequest)
conflGetContentResponseJSON = json.loads(conflGetContentResponse.read().decode('utf-8'))
print(conflGetContentResponseJSON)
    ##Si oui, on ne fait rien

    ##Si non, on écrase

        ##//On calcule la date du rapport

        ##//On constitue le titre

        ##//On constitue le HTML du rapport

        ##Publication