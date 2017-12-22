import tweepy #https://github.com/tweepy/tweepy
import csv
import time
#import test_tweet.py

#Twitter API credentials

consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

"""
consumer_key = "n3FJ2MnbyO5NZtU3ZTuCSTooZ"
consumer_secret = "mT8Xnq8PYQs3dB8pefXO9rGCW1yy1Ke4LNmeAHtMVLppuFSn2l"
access_key = "941339166503206912-b69lujbwgEZCOVDynqpHLECx5ciiqsF"
access_secret = "2Uoq5JwtixaYGxc2Igof3dHHyTUj22jD0PMD8D0XSnVhp"
"""
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

name = "YaoMing"
#name = 'Michaellee995'

sleeptime = 4
pages = tweepy.Cursor(api.followers, screen_name=name).pages()
direct = '/home/minghao/Downloads/big data proj/unsupervised/data_unsupervised'

limit = 500
with open(direct+'/userName_%s.csv' % name,'wb') as f:
	while True:
		try:
			page = next(pages)
			time.sleep(sleeptime)
			limit = limit - 1
			if limit == 0:
				break
		except tweepy.TweepError: #taking extra care of the "rate limit exceeded"
			time.sleep(60) 
			page = next(pages)
		except StopIteration:
			break
		for user in page:
			print(user.id_str)
			print(user.screen_name)
			print(user.followers_count)
			f.write(user.screen_name)
			f.write('\n')

"""
#name = "realDonaldTrump"
name = 'Michaellee995'
names = []
i = 0
for page in tweepy.Cursor(api.followers, screen_name=name).pages():
	if i>1:
		break
	print "a"
	try:
		user = page.
		names.extend(name)
		i += 1
		time.sleep(10)
	except:
		pass
print names
"""
