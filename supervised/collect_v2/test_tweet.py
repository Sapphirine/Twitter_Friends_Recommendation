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




fw=io.open("twitter_1129.txt",'w',encoding='utf8')

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
			with open('/home/minghao/Downloads/big data proj/data/python_12051310.json','a') as f:
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
	stop = stopwords.words('english') + punctuation +['rt','via','i','re','s']
	tweet = [term.lower() for term in tweet]
	terms_stop = [term for term in tweet 
					if term not in stop and
					ord(term[0])<128]
	return terms_stop

def display_json_tweet(file):
	count = 0

	client = MongoClient('localhost',27017)
	db = client.michael_2
	user = db.michael_2
	
	with open(file,'r') as f:
		with open("/home/minghao/Downloads/big data proj/supervised/data/output_12051310.csv",'wb') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames = ["original text","name", "content", "geo"], delimiter = ',')
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
				original = tweet['text']
				#del the emotions
				tokens = preprocess(tweet['text'])
				
				#del the stopwords
				texts = del_stop_word(tokens)
				rowstring = []
				for tok in texts:
					if '#' not in tok and '@' not in tok and 'http' not in tok:  #  Remove words with '@','#' and 'http' symbol
						rowstring.append(tok)

				#texts = [x.encode('utf-8') for x in rowstring]
				
				#texts = " ".join(texts)
				texts = " ".join(rowstring)
				letters_only = re.sub("[^a-zA-Z]"," ", texts)

				final_texts = "".join(letters_only)

				if geo[0]!=0:
					dic = {
						'name':tweet_id,
						'context':final_texts,
						'original texts':original,
						'geo':geo,
						'label':''
					}
					user.insert(dic)


				#create a list with all the terms
				terms_all = [term for term in final_texts.split()]

				#update the counter
				count_all.update(terms_all)
			except:
			 	pass
		#print the first 5 common frequent words
		print(count_all.most_common(20)) 

def save_to_mongodb(name,context,texts,geo):

	if geo[1]!='0':
		dic = {
			'name':name,
			'context':context,
			'original texts':texts,
			'geo':geo,
			'label':''
		}
		user.insert(dic)
	print "import completed!"          
