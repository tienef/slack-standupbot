import requests

class SlackClient:

    def __init__(self, url, token):
        self.url = url
        self.token = token

    def get(self, api, params):
        response = requests.get(self.url + api,
                                params=params)
        print(response.text)
        # self.logger.info(response.text)
        return response.json()

    def say(self):
        pass