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
                noAvater = False
            except:
                #print('No Avatar')
                a = 1
            if noAvatar == False:
                print(thisPerson['avatar'])
                for entry in output['items']:
                    psqlCur.execute("""INSERT INTO webexusers (
                        id,
                        title,
                        type,
                        isLocked,
                        lastActivity,
                        creatorId,
                        created,
                        avatar
                    ) VALUES (
                        '{id}',
                        '{title}',
                        '{type}',
                        '{islocked}',
                        '{lastactivity}',
                        '{creatorid}',
                        '{created}',
                        '{avatar}'
                    )""".format(
                        id = entry['id'],
                        title = entry['title'],
                        type = entry['type'],
                        islocked = entry['isLocked'],
                        lastactivity = entry['lastActivity'],
                        creatorid = entry['creatorId'],
                        created = entry['created'],
                        avatar = entry['avatar']
                    ))
                    print(entry)
