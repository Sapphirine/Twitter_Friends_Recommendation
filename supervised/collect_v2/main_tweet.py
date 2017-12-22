import test_tweet
from test_tweet import display_json_tweet
from test_tweet import MyListener
from tweepy import Stream
from test_tweet import save_to_mongodb
import tweepy,time,sys
from tweepy import OAuthHandler
import csv
from os.path import dirname, abspath

consumer_key=''
consumer_secret=''

access_token=''
access_secret=''

auth=OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_secret)

api=tweepy.API(auth)

#load tweets

#keyword = ["running","NBA","football","music","Times Square","swimming","Sephora","Coach","dumplings","Iphone X","sunshine","Thanks Giving","full stack","machine learning","Columbia"]
keyword = ['for']
#twitter_stream = Stream(auth,MyListener())
#twitter_stream.filter(track=keyword)
d = dirname(abspath(__file__))
display_json_tweet(d+"/data/python_12051310.json")
