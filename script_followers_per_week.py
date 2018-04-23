import tweepy
import json
import time
import os
import datetime

####Credenciales para uso del tweepy
consumer_key = 'WbaP94BKvPV0onNipttz8GxJh'
consumer_secret = 'sA3vrhAaUeHNKWDUHsbyURjRhjNIXrzw4Ns1buSnxIvrST4L42'
access_token = '2691538652-PLw61qVoUYHcAE2HiFN0FunRC9tVAcy5PgYC6nO'
access_token_secret = 'MjCh36tExJBtASapozPnlB3T2dhOZbqjLwzqTw0EsSYVO'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

#Abrimos el json
from pprint import pprint

path_to_json = '../visor-politico/public/json/twitter-candidatos-seguidores-semanales.json'

if os.path.isfile(path_to_json) and os.access(path_to_json, os.R_OK):
    jsonData = json.load(open(path_to_json))
else:
    with open(path_to_json, 'w') as outfile:
        js = {}
        json.dump(js, outfile)
    jsonData = json.load(open(path_to_json))

#Formato: #,Actor Politico, sede, cargo, nombre aspirante, genero, twitter
numero = 0
actor_politico = 1
sede = 2
cargo = 3
nombre = 4
genero = 5
twitter = 6

import csv
import sys
#Nombre del archivo
file_name = "candidatos.csv" 

#Abrimos el archivo como una lista de listas.
with open(file_name, 'rU') as f:
    reader = csv.reader(f)
    csvData = list(list(rec) for rec in csv.reader(f, delimiter=','))

#Removemos la cabezera
candidatos = csvData[1:]

print (jsonData)

for candidato in candidatos:
    if candidato[twitter] and not candidato[nombre] in jsonData:
        jsonData[candidato[nombre]] = [];

print(candidatos)
_now = datetime.datetime.now()
now = time.mktime(datetime.datetime(_now.year, _now.month , _now.day).timetuple()) * 1000

for candidato in candidatos:
    if candidato[twitter]:
        user = api.get_user(candidato[twitter])
        jsonData[candidato[nombre]].append([
            now,
            user.followers_count
    ]);

with open(path_to_json, 'w') as outfile:
    json.dump(jsonData, outfile)
print ("finished")
