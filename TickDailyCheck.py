from pymongo import mongo_client
import json

config = open('config.json')
setting = json.load(config)

MONGO_HOST = setting['MONGO_HOST']
MONGO_PORT = setting['MONGO_PORT']

def runCheck():
    pass
