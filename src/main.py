from standup.api.confluence import ConfluenceClient
from standup.api.slack import SlackClient
from standup.bot import StandUpBot
import argparse

# Définition et lecture des arguments
parser = argparse.ArgumentParser(description="Connecte le standup-bot au channel -c demandé et recueille les rapports de jour au format \"today xxxx\", \"yesterday xxxx\" "
                                             "ou \"obstacles xxxx\" et les enregistre dans le Confluence de Kepler dans l'espace -s sous la page -p demandée")
parser.add_argument("-c", "--channel", help="Nom du channel Slack où le bot doit se connecter pour lire les rapports du jour")
parser.add_argument("-s", "--space", help="Clé spaceKey de l'espace Confluence dans lequel stocker les rapports du jour")
parser.add_argument("-p", "--page", help="Nom de la page dans Confluence sous laquel les rapports seront stockés")
args = parser.parse_args()

# Slack
slackToken = "xoxb-89846243653-IAcQ287gmTpCB9xKcVkl1iKo"
slackServer = "https://slack.com"
slackChannel = args.channel

# Confluence
conflServer = "https://docs.kepler-rominfo.com"
conflUser = "thomas.faivre"
conflPassword = "thomas.faivre"
conflSpaceKey = args.space
conflMainContentName = args.page


if __name__ == '__main__':
    slack = SlackClient(slackServer, slackToken)
    confluence = ConfluenceClient(conflServer, conflUser, conflPassword)

    bot = StandUpBot(slack, confluence, conflSpaceKey, conflMainContentName, slackChannel)
    bot.run()