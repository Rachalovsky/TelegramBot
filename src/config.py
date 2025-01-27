from dotenv import dotenv_values

config = dotenv_values(".env.docker")

API_ID = config['API_ID']
API_HASH = config['API_HASH']

TG_TOKEN = config['TG_TOKEN']

POSTGRES_USER = config['POSTGRES_USER']
POSTGRES_PASSWORD = config['POSTGRES_PASSWORD']
POSTGRES_DATABASE = config['POSTGRES_DATABASE']
POSTGRES_HOST = config['POSTGRES_HOST']
POSTGRES_PORT = config['POSTGRES_PORT']
