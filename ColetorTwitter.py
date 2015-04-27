# -*- coding: utf-8 -*-

import sys
import tweepy
import webbrowser
import pymongo
import time

from tweepy.utils import import_simplejson

json = import_simplejson()

# Conectando ao MongoDB
try:
    conn=pymongo.MongoClient()
    print "Conectado com sucesso ao MongoDB!"
except pymongo.errors.ConnectionFailure, e:
   print "Não foi possível conectar ao MongoDB: %s" % e 

db = conn.mydb
collection = db[sys.argv[1]]

# Pegando a consulta por parâmetro

consulta = sys.argv[2:] 

#Autenticações

CONSUMER_KEY = 'ILHhQAC4QB0WNUdoRqmEA'
CONSUMER_SECRET = 'rmmkGo4YHniiJRwkwxGu9S7l5ZfhG7CZDXHw9eUo'
ACCESS_TOKEN = '339362662-rU6CizVcSZCr6CqWIhFh40yE0gmQdgusPRiwcpOj'
ACCESS_TOKEN_SECRET = 'CW9UCTOqYpzA1dS9doKcow6Bnz95UwZGBskcOsF2M6yIp'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


#Coletando tweets
class CustomStreamListener(tweepy.StreamListener):

    def on_data(self, status):
        
	#Carregando para o formato json
	tweet = json.loads(status)

	#Inserindo na coleção
	collection.insert(tweet)

	return True

    def on_error(self, status_code):
        print "Erro com o código:", status_code
        return True # Não mata o coletor

    def on_timeout(self):
        print "Tempo esgotado!"
        return True # Não mata o coletor

#Criando o coletor com timeout de 60 seg

streaming_api = tweepy.streaming.Stream(auth, CustomStreamListener(), timeout=60)
print "Coletando tweets sobre o tema ",consulta,":\n"
try:
	streaming_api.filter(follow=None, track=consulta)
except KeyboardInterrupt:
	print "\nColetor interrompido!"
