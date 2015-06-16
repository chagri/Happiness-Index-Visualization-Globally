import nltk
import re
import time
import urllib2
from urllib2 import urlopen
import cookielib
from cookielib import CookieJar
import datetime
import sqlite3

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/5')]

conn = sqlite3.connect('knowledgeBase.db')
c = conn.cursor()

startingWord = 'traffic'
stopwords = nltk.corpus.stopwords.words('english')
startingWordVal = 1
synArray = []

negativeWords = []
positiveWords = []

def main():
	try:
		page= 'http://thesaurus.com/browse/'+startingWord+'?s=t'
		sourceCode = opener.open(page).read()

		try:
			#print sourceCode
			synoNym = sourceCode.split('<div class="relevancy-list">')
			x=1
			while (x < len(synoNym)) :
				try:
					synoNymSplit = synoNym[x].split('</div>')[0]
					synoNyms = re.findall(r'\"\w*?">(\w*?)</span>', synoNymSplit)
					print synoNyms
					#time.sleep(555)
					for eachSyn in synoNyms:
						query = "Select * from wordVals Where word =?"
						c.execute(query, [(eachSyn)])
						data = c.fetchone()
						
						if data is None:
							print 'no data yet, we add them'
							c.execute("INSERT INTO wordVals (word,value) VALUES (?,?)", (eachSyn, startingWordVal))
							conn.commit()
						else:
							print 'word already exist'
								    
				except Exception,e:
					print str(e)
					print 'failed in 3rd try'
				x += 1

		except Exception,e:
			print str(e)
			print 'failed in 2nd try'
	
	except Exception, e:
		print str(e)
		print 'failed in the main loop'


main()
c.execute("INSERT INTO doneSyns (word, value) VALUES (?)", (startingWord))
conn.commit()
