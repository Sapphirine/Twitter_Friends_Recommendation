import tweepy #https://github.com/tweepy/tweepy
import csv
from preprocess import main
#import test_tweet.py

#Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

user = api.get_user(screen_name = 'KimKardashian')
print user.location
print user.lang
if user.location:
	print 1
else:
	print 0