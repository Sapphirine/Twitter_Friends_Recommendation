from sklearn.feature_extraction.text import CountVectorizer
from keras.models import load_model
import pandas as pd
import csv
import os
import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def classify(tweet):
	tweets = []
	tweets.append(tweet)
	train_data = pd.read_csv("Randombook_csv_train.csv", header=0,delimiter=",",quotechar='"', quoting=csv.QUOTE_ALL,names=['tweet','topic'])
	train_data_string=[]   # Initializing the string array to store appended train data
	for i in xrange( 0, train_data['tweet'].size ):
	    train_data_string.append(train_data['tweet'][i])
	Vectorizer = CountVectorizer(analyzer = "word",tokenizer = None,preprocessor = None,stop_words = 'english', max_features = 5000)
	train_data_string_transformed=Vectorizer.fit_transform(train_data_string)

	single_data_string_transformed = Vectorizer.transform(tweets)
	tweets_single = single_data_string_transformed.toarray()
	model_labeling = load_model('mymodel.h5')
	predited_topics = model_labeling.predict_classes(tweets_single, verbose=0)
	return predited_topics