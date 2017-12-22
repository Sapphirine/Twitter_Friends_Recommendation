import test_tweet
from test_tweet import preprocess
from test_tweet import del_stop_word
from test_tweet import del_word_started_by
import re
def main(text):
	tokens = preprocess(text)
	texts = del_stop_word(tokens)
	texts = ' '.join(filter(lambda x:x[0:4]!='http' 
		and x[0]!='@',texts))
	letters_only = re.sub("[^a-zA-Z]"," ", texts)
	final_texts = ''.join(letters_only)
	return final_texts

"""		
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