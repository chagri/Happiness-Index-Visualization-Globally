import tweepy as tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import requests
import time
import urllib
import sqlite3
import random
import simplejson
import subprocess as sp


conn = sqlite3.connect('wordBase.db')
c = conn.cursor()

NegWords5 = []
NegWords4 = []
NegWords3 = []
NegWords2 = []
NegWords1 = []

PosWords1 = []
PosWords2 = []
PosWords3 = []
PosWords4 = []
PosWords5 = []

stopWords = []
l = []
f = open("final2.txt", "w")

sql = "SELECT * FROM wordVal WHERE  value =?"

ckey = '**********Please Enter your key***********'
csecret = '***********Please Enter your secret*******************'
atoken = '*************Please Enter your auth****************'
asecret = '*************Please Enter your auth secret****************'

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = tweepy.API(auth)
f = open("output.csv","w")
def getWords():
	for negRow in c.execute(sql, [(-1)]):
		NegWords1.append(negRow[0])
	for negRow in c.execute(sql,[(-2)]):
		NegWords2.append(negRow[0])
	for negRow in c.execute(sql,[(-3)]):
		NegWords3.append(negRow[0])
	for negRow in c.execute(sql,[(-4)]):
		NegWords4.append(negRow[0])
	for negRow in c.execute(sql,[(-5)]):
		NegWords5.append(negRow[0])
	
	for posRow in c.execute(sql,[(1)]):
		PosWords1.append(posRow[0])
	for posRow in c.execute(sql,[(2)]):
		PosWords2.append(posRow[0])
	for posRow in c.execute(sql,[(3)]):
		PosWords3.append(posRow[0])
	for posRow in c.execute(sql,[(4)]):
		PosWords4.append(posRow[0])
	for posRow in c.execute(sql,[(5)]):
		PosWords5.append(posRow[0])

	for stopRow in c.execute(sql,[(0)]):
		stopWords.append(stopRow[0])

def browse(url, how_long):
	child = sp.Popen(["firefox", url])
	time.sleep(how_long)
	child.terminate()



class listener(StreamListener):
	
	def on_data(self, data):
		
		sentCounter = 0

		# Don't need this exception hadnling, just in case due to internet connection or something so that program doesn't close
		try:
			
			tweet = data.split(',"text":"')[1].split('","source')[0]
			location = data.split(',"location":"')[1].split('","url')[0]
			geo = data.split(',"geo":')[1].split(',"coordinates')[0]
			#user_id = data.split('"user":{"id":')[1].split(',"id')[0]
			coord = data.split(',"coordinates":')[1].split(',"place"')[0]
			pl = data.split(',"place":')[1].split(',"contrib')[0]
			place  = ""
			if (not geo is "null"):
				coord = coord.split('[')[1].split(']}')[0]
				temp_cord = coord.split(',')
				temp_cord = str(temp_cord[1])+','+str(temp_cord[0])
				#print temp_cord
			#print tweet+' '+location+' '+geo
			
			#saveThis = temp_cord+'\t'+location + '\t'
			#sentCounter = 0
		
			words = tweet.split()
			#print words
			for eachPosWord in PosWords1:
				if (eachPosWord in words):
					sentCounter += 1

			for eachPosWord in PosWords2:
				if (eachPosWord in words):
					sentCounter += 2

			for eachPosWord in PosWords3:
				if (eachPosWord in words):
					sentCounter += 3

			for eachPosWord in PosWords4:
				if (eachPosWord in words):
					sentCounter += 4

			for eachPosWord in PosWords5:
				if (eachPosWord in words):
					sentCounter += 5

			for eachNegWord in NegWords1:
				if (eachNegWord in words):
					sentCounter -= 1
				
			for eachNegWord in NegWords2:
				if (eachNegWord in words):
					sentCounter -= 2

			for eachNegWord in NegWords3:
				if (eachNegWord in words):
					sentCounter -= 3

			for eachNegWord in NegWords4:
				if (eachNegWord in words):
					sentCounter -= 4

			for eachNegWord in NegWords5:
				if (eachNegWord in words):
					sentCounter -= 5

			for eachStopWord in stopWords:
				if (eachStopWord in words):
					sentCounter += 0

			#final_cord = 'ST_SetSRID(ST_Point(\'' + cord + '\'),4326))&api_key=db39d3aa5e0249ab0de7d29d48a0854501f0cca2'
			while sentCounter is not 0:
				url = "http://clokar.cartodb.com/api/v2/sql?q=INSERT INTO exp_geo (tweet,geo,the_geom,senti_score) VALUES('" + tweet+ "','"+location+"',ST_SetSRID(ST_Point(" + temp_cord + "),4326)," + str(sentCounter) + ")&api_key=db39d3aa5e0249ab0de7d29d48a0854501f0cca2"
				#print url
				browse(url, 1)

				if (location != "" or geo != "null"):
					#print sentCounter, " ::::: " + saveThis
					a=1
				f.write(str(sentCounter))
				f.write(',')
				sentCounter = 0

				saveFile = open('final_output.tsv', 'a') # From here till close it is for saving the data
				#saveFile.write(saveThis)
				saveFile.write('\n')
				saveFile.close()
			return True
			
		
		except BaseException, e:
			print 'failed on data, ', str(e)
			time.sleep(5)
	
	def on_error(self, data):
		print data

getWords()
twitterStream = Stream(auth, listener())
#twitterStream.filter(track=["good"])
twitterStream.filter(locations=[-160,-49,163,73], async=False)
##These coordinates are approximate bounding box around USA


