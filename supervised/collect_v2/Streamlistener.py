from __future__ import print_function
import tweepy
import json
from pymongo import MongoClient
from labeling import classify
from test_tweet import preprocess, del_stop_word
from dateutil import parser
import re

MONGO_HOST = 'mongodb://localhost:27017/twitterfinal'  # assuming you have mongoDB installed locally


class StreamListener(tweepy.StreamListener):    
    #This is a class provided by tweepy to access the Twitter Streaming API. 

    def on_connect(self):
        # Called initially to connect to the Streaming API
        print("You are now connected to the streaming API.")
 
    def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        print('An Error has occured: ' + repr(status_code))
        return False
 
    def on_data(self, data):
        #This is the meat of the script...it connects to your mongoDB and stores the tweet
        try:
            client = MongoClient(MONGO_HOST)
            
            # Use twitterdb database. If it doesn't exist, it will be created.
            db = client.twitterfinal
    
            # Decode the JSON from Twitter
            datajson = json.loads(data)

            #context extraction
            geo = datajson.get('coordinates')
            if geo:
                flag = 0
                geo = geo['coordinates']
                timestamp = parser.parse(datajson['created_at'])
                timestamp = timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')

                text = datajson['text']
		#print (text)

                #del the emotions 
                tokens = preprocess(text)

                #del the stop words
                texts = del_stop_word(tokens)

                rowstring = []
                for tok in texts:
                    if '#' not in tok and '@' not in tok and 'http' not in tok:  #  Remove words with '@','#' and 'http' symbol
                        rowstring.append(tok)
                    if "job" in tok:
                        flag = 1
		    if "hiring" in tok:
			flag = 1
                    if "photo" in tok:
                        flag = 2
		    if "video" in tok:
			flag = 2

                texts = " ".join(rowstring)
                letters_only = re.sub("[^a-zA-Z]"," ", texts)
                final_texts = "".join(letters_only)
		print (final_texts)

                label = classify(final_texts)
                label_num = label[0]
                if label_num == 0:
                    label_final = 'Sports'
                elif label_num == 1:
                    label_final = 'Entertainments'
                elif label_num == 2:
                    label_final = 'Politics'
                elif label_num == 3:
                    label_final = 'Education'
                elif label_num == 4:
                    label_final = 'Technology'
                elif label_num == 5:
                    label_final = 'Business'

                if flag == 1:
                    label_final = 'Job_searching'
                elif flag == 2:
                    label_final = 'Entertainments'



                result = {
                    'user': datajson['user']['screen_name'],
                    'original_text': datajson['text'],
                    'processed_text': final_texts,
                    'geo' : geo,
                    'time': timestamp,
                    'label': label_final
                }
                print (result)
                tweet = json.dumps(result)
                print (1)

            
                #insert the data into the mongoDB into a collection called twitter_search
                #if twitter_search doesn't exist, it will be created.
                db.twitter_search.insert(result)
                print("inserted one more tweet")
        except Exception as e:
           print(e)

