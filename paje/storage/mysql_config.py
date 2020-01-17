import json

config = {}

with open('paje/storage/mysql_config.json') as fd:
    config = json.load(fd)
