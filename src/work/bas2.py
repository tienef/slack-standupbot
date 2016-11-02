"""
import urllib.request
import json

conflUser = "thomas.faivre"
conflPassword = "thomas.faivre"

r = urllib.request.get('http://localhost:8080/confluence/rest/api/content',
	params={'title' : 'Page title to comment on'},
	auth=(conflUser, conflPassword))

printResponse(r)
"""

import requests, json

conflServer = "https://docs.kepler-rominfo.com"
conflContentId = "24740688"
conflUser = "thomas.faivre"
conflPassword = "thomas.faivre"


r = requests.get(conflServer+'/rest/api/content',
	params={'title' : 'Functional'},
	auth=(conflUser, conflPassword))

print(r.json())

"""
parentPage = r.json()['results'][0]
pageData = {'type':'comment', 'container':parentPage,
	'body':{'storage':{'value':"<p>A new comment</p>",'representation':'storage'}}}
r = requests.post('http://localhost:8080/confluence/rest/api/content',
	data=json.dumps(pageData),
	auth=('admin','admin'),
	headers=({'Content-Type':'application/json'}))
printResponse(r)
"""