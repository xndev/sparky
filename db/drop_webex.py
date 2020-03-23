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
cur.execute('DROP TABLE webexusers')
conn.close()

print('DB deleted!')
