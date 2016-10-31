import requests


class ConfluenceClient:

    def __init__(self, url, login, password):
        self.url = url
        self.login = login
        self.password = password

    def get_page(self, title):
        return self.get('/rest/api/content', {
            "title": title
        })

    def get(self, api, params):

        response = requests.get(self.url + api,
                         params=params,
                         auth=(self.login, self.password))

        print(response.text)
        #self.logger.info(response.text)

        return response.json()
