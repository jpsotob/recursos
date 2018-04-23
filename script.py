import tweepy
import json
import time

####Credenciales para uso del tweepy
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

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
    data = list(list(rec) for rec in csv.reader(f, delimiter=','))

#Removemos la cabezera
candidatos = data[1:]

json_file = {}

for candidato in candidatos:
    if candidato[twitter]:
        user = api.get_user(candidato[twitter])
        json_file[candidato[nombre]] = {
            "actor_politico": candidato[actor_politico],
            "sede": candidato[sede],
            "cargo": candidato[cargo],
            "name": user.name,
            "genero": candidato[genero],
            "twitter": candidato[twitter],
            "followers": user.followers_count,
            "picture": user.profile_image_url.replace("_normal","")
        }
    else:
        json_file[candidato[nombre]] = {
            "actor_politico": candidato[actor_politico],
            "sede": candidato[sede],
            "cargo": candidato[cargo],
            "genero": candidato[genero],
            "twitter": candidato[twitter],
            "followers": 0,
            "picture": "../img/no_image.png"
        }

with open('../visor-politico/public/json/twitter-candidatos-seguidores.json', 'w') as outfile:
    json.dump(json_file, outfile)
print ("finished")
