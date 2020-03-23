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

r = requests.get('https://api.ciscospark.com/v1/rooms',
                  headers={'Authorization': 'Bearer {auth}'.format(auth=webexAuth)})
binary = r.content
output = json.loads(binary)

for entry in output['items']:
    psqlCur.execute("""INSERT INTO webexusers (
        id,
        title,
        type,
        isLocked,
        lastActivity,
        creatorId,
        created
    ) VALUES (
        '{id}',
        '{title}',
        '{type}',
        '{islocked}',
        '{lastactivity}',
        '{creatorid}',
        '{created}'
    )""".format(
        id = entry['id'],
        title = entry['title'],
        type = entry['type'],
        islocked = entry['isLocked'],
        lastactivity = entry['lastActivity'],
        creatorid = entry['creatorId'],
        created = entry['created']
    ))
    print(entry)
