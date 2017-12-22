import tweepy,time,sys
from tweepy import OAuthHandler
from tweepy import Stream 
from tweepy.streaming import StreamListener
from nltk.corpus import stopwords
import operator 
from collections import Counter
from pymongo import MongoClient
import json
import io
import re
import string
import csv



fw=io.open("twitter_1119.txt",'w',encoding='utf8')

consumer_key=''
consumer_secret=''

access_token=''
access_secret=''

auth=OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_secret)

api=tweepy.API(auth)
 
emoticons_str = r"""
	(?:
		[:=;] # Eyes
		[oO\-]? # Nose (optional)
		[D\)\]\(\]/\\OpP] # Mouth
	)"""
 
regex_str = [
	emoticons_str,
	r'<[^>]+>', # HTML tags
	r'(?:@[\w_]+)', # @-mentions
	r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
	r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs

	r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
	r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
	r'(?:[\w_]+)', # other words
	r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
def tokenize(s):
	return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):

	tokens = tokenize(s)
	if lowercase:
		tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
	return tokens

class MyListener(StreamListener):

	def on_data(self,data):
		try:
			with open('S:\\python_11191730.json','a') as f:
				print data,'\n'
				f.write(data)
				return True
		except BaseException as e:
			print ("Error on_data: %s" % str(e))
		return True

	def on_error(self,status):
		print (status)
		return True
def process_or_store(tweet):
	print json.dumps(tweet)                                                 #use tweet['text'] to print only the text part

def read_tweets():

	for status in tweepy.Cursor(api.home_timeline).items(10):   #to read tweets from timeline
		fw.write(status.text+"\n")
		process_or_store(status._json)

	for tweet in tweepy.Cursor(api.user_timeline).items():
		fw.write(tweet.text+"\n")
		process_or_store(tweet._json)


	"""for friend in tweepy.Cursor(api.friends).items():                   #to get the list of followers
		fw.write(friend.name+"\n")
		process_or_store(friend._json)"""

	"""for tweet in tweepy.Cursor(api.user_timeline).items(10):          #to get our tweets
		process_or_store(tweet._json)"""

	fw.close()                                                           #use when using first function to write timeline tweets



def post_tweet(tweet,num,min):                                                      #function to tweet on twitter

	i=0
	while i<num:
		api.update_status(status=tweet)
		time.sleep(min*60)                                          #tweet 10 times after every 10 mins

def del_symbols(tweet):
	tweet = json.dumps(tweet)
	punctuation = "!\"#$%&'()*+,-./:;<=>?@[]^_`{|}~"
	tweet = ''.join(ch for ch in tweet if ch not in punctuation)
	tweet = ' '.join(filter(lambda x:x[0]!='\\',tweet.split()))
	tweet = ' '.join(filter(lambda x:x[0]!='.',tweet.split()))
	tweet = ' '.join(filter(lambda x:x[0]!=':',tweet.split()))
	#tweet = ' '.join(filter(lambda x:x[0:5]!='https',tweet.split()))
	tweet = tweet.lower()
	return tweet

def del_stop_word(tweet):
	#tweet = tweet.lower()
	punctuation = list(string.punctuation)
	stop = stopwords.words('english') + punctuation +['RT','via']
	terms_stop = [term for term in tweet 
					if term not in stop and
					ord(term[0])<128]
	return terms_stop

def del_word_started_by(tweet):
	texts = " ".join(filter(lambda x:x[0:4]!='https'),texts.split(" "))
	return texts

def display_json_tweet(file):
	count = 0
	with open(file,'r') as f:
		with open("output_11191730.csv",'wb') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames = ["name", "content", "geo"], delimiter = ',')
			writer.writeheader()
		count_all = Counter()
		for line in f:
			try:				
				line = line.decode("utf-8")
				tweet = json.loads(line)    #load it as pyhton dict
				#print 1
				#print tweet
				
				tweet_id = tweet['user']['screen_name']
				#tweet_id = [x.encode('utf-8') for x in tweet_id]
				#print tweet_id

				if tweet['place']:
					lon = tweet['place']['bounding_box']['coordinates'][0][0][0]
					lat = tweet['place']['bounding_box']['coordinates'][0][0][1]
					#['bounding_box']['coordinates']
				else:
					lon = 0
					lat = 0
				geo = [lat,lon]
				#print geo

				#del the emotions
				tokens = preprocess(tweet['text'])
				
				#del the stopwords
				texts = tokens = del_stop_word(tokens)
				texts = [x.encode('utf-8') for x in texts]
				texts = " ".join(texts)
				#print texts

				#create a list with all the terms
				terms_all = [term for term in tokens]

				#update the counter
				count_all.update(terms_all)

				RESULT = [tweet_id,texts,geo]
				#RESULT = [x.encode('utf-8') for x in RESULT]
				print RESULT
				with open("output_11191730.csv",'ab') as resultFile:
					wr = csv.writer(resultFile)
					wr.writerow(RESULT)
			except:
			 	pass
		#print the first 5 common frequent words
		print(count_all.most_common(5)) 

def save_to_mongodb(filename,keyword):
	client = MongoClient('localhost',27017)
	db = client.Michael
	user = db.Michael
	with open(filename,'rb') as f:
		for line in f:
			name = line[0]
			context = line[1]
			geo = line[2]
			dic = {
				'name':name,
				'context':context,
				'geo':geo,
				'label':keyword
			}
			user.insert(dic)
	print "import completed!"          