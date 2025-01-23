from dotenv import dotenv_values

config = dotenv_values("../.env")

API_ID = config['API_ID']
API_HASH = config['API_HASH']

TG_TOKEN = config['TG_TOKEN']

DATABASE_URL = config['DATABASE_URL']

PG_USER = config['PG_USER']
PG_PASSWORD = config['PG_PASSWORD']
PG_DATABASE = config['PG_DATABASE']
PG_HOST = config['PG_HOST']
PG_PORT = config['PG_PORT']
