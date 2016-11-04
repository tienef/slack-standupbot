from standup.api.confluence import ConfluenceClient
from standup.api.slack import SlackClient
from standup.bot import StandUpBot
import argparse

# Définition et lecture des arguments
parser = argparse.ArgumentParser(description="Connects standup-bot to -c channel of Slack using -t token. Collects"
                                             " messages of the day having format \"today xxxx\", \"yesterday xxxx\" "
                                             "or \"obstacles xxxx\" and save them in Confluence -s server in space "
                                             "having -k key under page name -n. -u User and -p Password for Confluence"
                                             " must also be provided. Designed for Confluence 5.9.2")
parser.add_argument("-c", "--channel", help="Name of Slack channel where bot must connect to collect messages")
parser.add_argument("-k", "--key", help="SpaceKey of Confluence space where daily reports will be generated")
parser.add_argument("-n", "--nameofconfluencepage", help="Name of Confluence page under daily reports will be generated")
parser.add_argument("-t", "--token", help="Slack token")
parser.add_argument("-s", "--serverconfluence", help="Confluence Server. Example : \"https://docs.myconfluenceserver.com\"")
parser.add_argument("-u", "--userconfluence", help="Confluence user to connect with")
parser.add_argument("-p", "--passwordconfluence", help="Password password to connect with")

args = parser.parse_args()

# Slack
slackToken = args.token
slackServer = "https://slack.com"
slackChannel = args.channel

# Confluence
conflServer = args.serverconfluence
conflUser = args.userconfluence
conflPassword = args.passwordconfluence
conflSpaceKey = args.space
conflMainContentName = args.page


if __name__ == '__main__':
    slack = SlackClient(slackServer, slackToken)
    confluence = ConfluenceClient(conflServer, conflUser, conflPassword)

    bot = StandUpBot(slack, confluence, conflSpaceKey, conflMainContentName, slackChannel)
    bot.run()