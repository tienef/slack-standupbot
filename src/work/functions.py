import urllib.request
import json

##Confluence
conflServer = "'https://docs.kepler-rominfo.com/rest/api/"
conflContentId = "24740688"
conflUser = "thomas.faivre"
conflPassword = "thomas.faivre"

# create a password manager
password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()

# Add the username and password.
# If we knew the realm, we could use it instead of None.

password_mgr.add_password(None, conflServer, conflUser, conflPassword)

handler = urllib.request.HTTPBasicAuthHandler(password_mgr)

# create "opener" (OpenerDirector instance)
opener = urllib.request.build_opener(handler)

# use the opener to fetch a URL
##opener.open(conflServer)

# Install the opener.
# Now all calls to urllib.request.urlopen use our opener.
urllib.request.install_opener(opener)
title = "Functional"

conflGetContentResponse = urllib.request.urlopen('https://docs.kepler-rominfo.com/rest/api/content?title=Functional')

conflGetContentResponseJSON = json.loads(conflGetContentResponse.read().decode('utf-8'))
print(conflGetContentResponseJSON)