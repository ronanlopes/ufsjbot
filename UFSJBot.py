# -*- coding: utf-8 -*-

import sys
import tweepy
import webbrowser
import time

reload(sys)
sys.setdefaultencoding("utf-8")

# Pegando a consulta por parâmetro

consulta = sys.argv[1:] 

#Autenticações

consumer_key = 'w8FmJROsBCnoirSqZxZbg'
consumer_secret = 'PoPc3qVdDWYzYHAo22xqnLfPXQdS2TLa8iucBLOqk'
access_token = '1870359661-4pv55A2ZSPQ6UmZR1vpZNcAXXOlRZ67AH9kLClf'
access_token_secret = 'yoCh8kLPon51FIookFfvs3ka3H6W6c5ZMD1Lgb5Mk8B96'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth) 

#Coletando tweets
class CustomStreamListener(tweepy.StreamListener):

    def on_status(self, tweet):
	autor = str(tweet.author.screen_name)
	texto = str(tweet.text)
	idtweet = str(tweet.id)
	link = "http://www.twitter.com/"+autor+"/status/"+idtweet
	if (tweet.text[0:2]!='RT' and autor!="UFSJBot"):
		if (len(autor)+len(texto)>131):
			texto = texto[0:127-len(autor)-len(link)]+"..."
			tweet_bot = "Por @"+autor+": \""+texto+"\" "+link
		else:
			tweet_bot = "Por @"+autor+": \""+texto+"\""
		
		api.update_status(tweet_bot)
		print "\n@"+autor+" mencionado. Dormindo por 60 segundos..."
		time.sleep(60)
		print "\nVoltando a coletar..."

	return True

    def on_error(self, status_code):
        print "Erro com o código:", status_code
        return True # Não mata o coletor

    def on_timeout(self):
        print "Tempo esgotado!"
        return True # Não mata o coletor

#Criando o coletor com timeout de 60 seg

streaming_api = tweepy.streaming.Stream(auth, CustomStreamListener(), timeout=60)
print "Coletando tweets... "
try:
	streaming_api.filter(follow=None, track=consulta)
except KeyboardInterrupt:
	print "\nBot interrompido!"

