import psycopg2
import configparser
import requests
import json
import pprint

config = configparser.RawConfigParser()
config.read('/var/www/settings.ini')
psqlUser = config['POSTGRES']['user']
psqlPass = config['POSTGRES']['pass']
psqlDb = config['POSTGRES']['db']
webexAuth = config['AARON']['Token']

psqlConn = psycopg2.connect(database=psqlDb, user=psqlUser, host='localhost', password=psqlPass)
psqlConn.autocommit = True
psqlCur = psqlConn.cursor()
urlWebex = 'https://api.ciscospark.com/v1/'

r = requests.get('{url}organizations'.format(url=urlWebex),
        headers={'Authorization': 'Bearer {auth}'.format(auth=webexAuth)})
_output = r.content
output = json.loads(_output)
#print(output)
for thisOrg in output['items']:
    #print(thisOrg['id'])
    #print(thisOrg['displayName'])
    rGetPeopleOrg = requests.get('{url}people?orgId={id}'.format(url=urlWebex, id=thisOrg['id']),
        headers={'Authorization': 'Bearer {auth}'.format(auth=webexAuth)})
    _output = rGetPeopleOrg.content
    output = json.loads(_output)
    #print(output)
    for thisPerson in output['items']:
        if str(thisPerson['id']) != 'Y2lzY29zcGFyazovL3VzL1BFT1BMRS8wNGEzOTA1NC04NjQ3LTQ2YWQtYjJmOS0zNTEwYzhkOGUxNDA':
            #print(str(thisPerson))
            #print(str(thisPerson['id']))
            #print(str(thisPerson['displayName']))
            noAvatar = True
            try:
                print(str(thisPerson['avatar']))
                noAvatar = False
            except:
                #print('No Avatar')
                a = 1
            if noAvatar == False:
                print(thisPerson['id'])
                print(thisPerson['avatar'])
                psqlCur.execute("""INSERT INTO webexusers (
                    id,
                    avatar
                ) VALUES (
                    '{id}',
                    '{avatar}'
                )""".format(
                    id = thisPerson['id'],
                    avatar = thisPerson['avatar']
                ))
