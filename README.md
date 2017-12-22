# Twitter_Friends_Recommendation
Big Data Analysis Project: Friends Recommendation in Twitter

Group Member: Minghao Li(ml4025), Bicheng Jiang(bj2376), Qi Zheng(qz2306)

Abstract:
The objectives of this project include Big data analysis
for both practical use and theoretical results: we applied two
learning algorithm to three dataset, two of which are crawled
by ourselves; based on the result of comparison, we utilized the
supervised learning algorithm on the backend of our website,
which is written in node js and deployed on Amazon EC2
instance. Firstly, for the supervised learning, we collected realtime
data from tweepy API, did the customized context clean,
added the labels based on the model which are trained out from
Neural Network Algorithm and stored it into the database; for
the unsupervised learning, we used different collection but the
same processing method to deal with it and trained using Kmeans
algorithm. Then we developed a website using the node
framework, which keep updating the front end data according to
that in database. At last, the website were deployed to Amazon
EC2 instance for public access.

Program running:
1. website: 
  a. cd ~/nodejs 
  b. run "npm install"
  c. open the url "localhost:2222" to see the result.

2. data collections:
  a. Data collection for the supervised learning. The dataset from online is  in the supervised/collect_v2 folder.
  b. The real-time tweet collection is by running the backprocess.py file. Simply type in your own Twitter API keys in the correct location, the program can run the whole stuff, including the streaming, processing, filtering, labeling and storing.

3. User Cluster:
  a. run the collect_userid.py and then tweet_dumper.py for the tweets of 300 hundrd follwers of one famous user, who can be assiged in the collect_userid.py. The result will be automatically stored in result_test.csv. Then simply run the backup.ipynb, you can get the result.

4. Neural Network Training: 
  a. We have trained the model ready for you, named as mymodel.h5. The real-time tweet collection will do the labeling process by itself. No more operations are needed here. 
 
Youtube Link:
