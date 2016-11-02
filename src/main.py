from standup.api.confluence import ConfluenceClient
from standup.api.slack import SlackClient
from standup.bot import StandUpBot

##Slack
slackToken = "xoxb-89846243653-IAcQ287gmTpCB9xKcVkl1iKo"
slackServer = "https://slack.com"

##Confluence
conflServer = "https://docs.kepler-rominfo.com"
conflMainContentId = "24740688"
conflUser = "thomas.faivre"
conflPassword = "thomas.faivre"
conflSpaceKey = "PATDMT"


if __name__ == '__main__':
    slack = SlackClient(slackServer, slackToken)
    confluence = ConfluenceClient(conflServer, conflUser, conflPassword)

    bot = StandUpBot(slack, confluence, conflSpaceKey, conflMainContentId)
    bot.run()