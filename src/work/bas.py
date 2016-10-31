import urllib.request
import json
import base64
##base64string = base64.encodebytes('%s:%s' % (username, password))[:-1]
##req.add_header("Authorization", "Basic %s" % base64string)

##Confluence
conflServer = "https://docs.kepler-rominfo.com"
conflContentId = "24740688"
conflUser = "thomas.faivre"
conflPassword = "thomas.faivre"

title = 'Functional'

p = urllib.request.HTTPPasswordMgrWithPriorAuth()

p.add_password(None,"https://docs.kepler-rominfo.com/rest/api/content?title=Functional", conflUser, conflPassword, is_authenticated=False)
auth_handler = urllib.request.HTTPBasicAuthHandler(p)
opener = urllib.request.build_opener(auth_handler)
urllib.request.install_opener(opener)

conflGetContentRequest = urllib.request.Request(
            url=conflServer + '/rest/api/content?title=%(title)s' % {
                'title': title}, method='GET')
print(conflGetContentRequest)
x = opener.open("https://docs.kepler-rominfo.com/rest/api/content?title=Functional")
print(x.read())

##conflGetContentResponse = urllib.request.urlopen(conflGetContentRequest)
##conflGetContentResponseJSON = json.loads(conflGetContentResponse.read().decode('utf-8'))
##print(conflGetContentResponseJSON)

