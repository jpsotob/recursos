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

path_to_json = '../visor-politico/public/json/twitter-candidatos-datos-semanales.json'

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
        jsonData[candidato[nombre]] = {}
        jsonData[candidato[nombre]]["seguidores"] = []
        jsonData[candidato[nombre]]["tweets"] = []
        jsonData[candidato[nombre]]["tweets_semana"] = []



_now = datetime.datetime.now()

_date = (datetime.date.today() - datetime.timedelta(days=7))

now = time.mktime(datetime.datetime(_now.year, _now.month , _now.day).timetuple()) * 1000

for candidato in candidatos:
    if candidato[twitter]:
        user = api.get_user(candidato[twitter])
        count = 0

        startDate = datetime.datetime(_date.year, _date.month, _date.day, 0, 0, 0)

        tweets = []
        cond = True
        page = 0
        while cond:
            page += 1
            tmpTweets = api.user_timeline(user.id, page=page)
            for tweet in tmpTweets:
                if tweet.created_at > startDate:
                    count +=1
                    tweets.append(tweet)
                else:
                    cond = False
                    break

        print(len(tweets))
        jsonData[candidato[nombre]]["seguidores"].append([
            now,
            user.followers_count
        ])
        jsonData[candidato[nombre]]["tweets"].append([
            now,
            user.statuses_count
        ])
        jsonData[candidato[nombre]]["tweets_semana"].append([
            now,
            count
        ])
        
        

print(jsonData)
with open(path_to_json, 'w') as outfile:
    json.dump(jsonData, outfile)
print ("finished")
