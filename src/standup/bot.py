
class StandUpBot:

    def __init__(self, slackClient, confluenceClient):
        self.slack = slackClient
        self.confluence = confluenceClient

    def run(self):
        print ("Toto")
