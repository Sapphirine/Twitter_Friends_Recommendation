#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv
from preprocess import main
from os.path import dirname, abspath
#import test_tweet.py

#Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""


def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	result = []
	
	#make initial request for most recent tweets (200 is the maximum allowed count)

	user = api.get_user(screen_name = screen_name)
	location = user.location
	lang = user.lang
	print location
	if location and lang =="en":
		print 1

		new_tweets = api.user_timeline(screen_name = screen_name,count=200)
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#save the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		#keep grabbing tweets until there are no tweets left to grab
		while len(new_tweets) > 0:
			#print "getting tweets before %s" % (oldest)
			
			#all subsiquent requests use the max_id param to prevent duplicates
			new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

			#save most recent tweets
			alltweets.extend(new_tweets)
			#update the id of the oldest tweet less one
			oldest = alltweets[-1].id - 1
			
			#print "...%s tweets downloaded so far" % (len(alltweets))
		
		#transform the tweepy tweets into a 2D array that will populate the csv	
		#outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8"),screen_name] for tweet in alltweets]
		x=0
		for count in range(len(alltweets)):
			char = alltweets[count].text.encode("utf-8")
			char = main(char)
			result.append(char)
		#outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8"),screen_name] for tweet in alltweets]
		outtweets = [[alltweets[i].id_str, alltweets[i].created_at, result[i], location, screen_name] for i in range(len(alltweets))]
		
		#write the csv
		direct = '/home/minghao/Downloads/big data proj/unsupervised/data_unsupervised'	
		d = dirname(dirname(abspath(__file__)))
		with open(direct+'/%s_tweets.csv' % screen_name, 'wb') as f:
			writer = csv.writer(f)
			writer.writerow(["id","created_at","text","location","screen_name"])
			writer.writerows(outtweets)
		
		pass


if __name__ == '__main__':
	names = []
	direct = '/home/minghao/Downloads/big data proj/unsupervised/data_unsupervised'
	#pass in the username of the account you want to download
	with open(direct+'/userName_YaoMing.csv','rb') as namefile:
		for line in namefile:
			line = line.replace('\n','')
			names.append(line)
	for item in names:
		print item
		try:
			get_all_tweets(item)
		except:
			pass
	
	count = 1
	with open(direct+'/result_test.csv','ab') as fout:
		for item in names:
			try:	
				with open(direct+'/%s_tweets.csv' % item, 'rb') as f:
					if count == 0:
						for line in f:
							fout.write(line)
							count += 1
					else:
						f.next()
						for line in f:
							fout.write(line)
			except:
				pass

""" as  for one line, but with restrictions: too long to be able to store in one line		
if __name__ == '__main__':
	#pass in the username of the account you want to download
	names = ['BenSimmons25','KingJames','JohnMaraJr']
	for item in names:
		get_all_tweets(item)
	direct = 'S:/OneDrive/Documents/Big Data Analytics/final project/data'
	result = ""
	with open(direct+'/result.csv','a') as fout:
		writer = csv.writer(fout)
		for item in names:	
			with open(direct+'/%s_tweets.csv' % item, 'r') as f:
				f.next()
				for line in f:
					word = line.split(",")[2].strip()
					result=result+word
				row = [result,item]
				writer.writerow(row)
"""
