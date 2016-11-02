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

    def get_contentId_from_title(self, title, spacekey):
        response = self.get_content("/rest/api/content", {"title": title, "spaceKey": spacekey})
        if len(response["results"]) > 1:
            print("Il existe plusieurs pages portant ce nom dans Confluence !")
            return False
        if len(response["results"]) == 1:
            return {"contentId" : response["results"][0]["id"],
                    "version" : response["results"][0]["_expandable"]["version"]}
        else:
            print("Aucune page ne porte ce nom dans Confluence !")
            return False

    def create_content(self, api, json):

        response = requests.post(self.url + api,
                                 json=json,
                                 auth=(self.login, self.password),
                                )
        print(response.text)
        # self.logger.info(response.text)
        return response.json()


    def update_content(self, api, json):
        response = requests.put(self.url + api,
                                json=json,
                                auth=(self.login, self.password),
                                )
        print(response.text)
        # self.logger.info(response.text)
        return response.json()