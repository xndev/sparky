import configparser
import psycopg2

config = configparser.RawConfigParser()
config.read('/var/www/settings.ini')
authPsqlUser = config['POSTGRES']['user']
authPsqlPass = config['POSTGRES']['pass']
authPsqlDb = config['POSTGRES']['db']

conn = psycopg2.connect(database=authPsqlDb, user=authPsqlUser, host='localhost', password=authPsqlPass)
conn.autocommit = True
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS webexusers (
    id TEXT,
    title TEXT,
    type TEXT,
    isLocked BOOLEAN,
    lastActivity TEXT,
    teamId TEXT,
    creatorId TEXT,
    created TEXT,
    ownerId TEXT,
    avatar TEXT
)""")

conn.close()

print('DB created or already exists')
