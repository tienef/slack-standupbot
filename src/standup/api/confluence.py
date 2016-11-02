import requests

class ConfluenceClient:

    def __init__(self, url, login, password):
        self.url = url
        self.login = login
        self.password = password

    def get_content(self, api, params):

        response = requests.get(self.url + api,
                         params=params,
                         auth=(self.login, self.password))
        print(response.text)
        #self.logger.info(response.text)

        return response.json()