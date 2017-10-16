__author__ = 'adnan'

#This program is based on twitter Rest api. It takes two inputs, 1)name of the user 2)hashtags with which filter is applied.
#It extracts historical tweets from user timeline (up to 16*200) and pre-proces it and filter the tweets with the i/p hashtag.
#It applies sentiment analysis and outputs the user review about it. consider following example;
#python user_timeline_sentiment_updated.py garin_harris \#colorrun
#garin_harris is the users twitter handle and #colorrun is the event name.

#This program will extract all tweets in which user mentioned #colorrun and will output if he has positive review or negative review about the event.


import sys
import re
import string
import time
import config
import json
import twitter_sentiment
from tweepy import Cursor
from tweepy import OAuthHandler
from tweepy import API
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from textblob import TextBlob
import pandas as pd


def process(text, tokenizer=TweetTokenizer(), stopwords=[]):
	text = text.lower()
	tokens = tokenizer.tokenize(text)
	return [tok for tok in tokens if tok not in stopwords and not tok.isdigit()]


def clean_tweet(tweet):
	'''
	Utility function to clean tweet text by removing links, special characters
	using simple regex statements.
	'''
	return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())



def get_tweet_polarity_score(tweet):
	'''
	Utility function to get polarity score from tweets
	'''
	# create TextBlob object of passed tweet text
	analysis = TextBlob(clean_tweet(tweet))
	return analysis.sentiment.polarity


def get_tweet_sentiment(tweet):
	'''
	Utility function to classify sentiment of passed tweet
	using textblob's sentiment method
	'''
	# create TextBlob object of passed tweet text
	analysis = TextBlob(clean_tweet(tweet))
	# set sentiment
	if analysis.sentiment.polarity > 0:
		return 'positive'
	elif analysis.sentiment.polarity == 0:
		return 'neutral'
	else:
		return 'negative'







if __name__ == '__main__':

	user = sys.argv[1]
	query = sys.argv[2].lower()
	auth = OAuthHandler(config.consumer_key, config.consumer_secret)
	auth.set_access_token(config.access_token, config.access_secret)
	client= API(auth)
	tweet_tokenizer = TweetTokenizer()
	punct = list(string.punctuation)
	stopword_list = stopwords.words('english') + punct + ['rt','via','...']
	tweets = []
	 
	

	for page in Cursor(client.user_timeline, screen_name=user, count=200).pages(16):
		for status in page:
			text = status.text
			tokens = process(text, tokenizer=tweet_tokenizer, stopwords=stopword_list)
			if query in tokens:

				parsed_tweet = {}
				# saving text of tweet
				parsed_tweet['text'] = status.text
				# saving sentiment of tweet
				parsed_tweet['sentiment'] = get_tweet_sentiment(status.text)
				# saving polarity score
				parsed_tweet['score'] = get_tweet_polarity_score(status.text)

				# appending parsed tweet to tweets list
				if status.retweet_count > 0:
					# if tweet has retweets, ensure that it is appended only once
					if parsed_tweet not in tweets:
						tweets.append(parsed_tweet)
				else:
					tweets.append(parsed_tweet)



	print ("Total number of tweets with {}: {}".format(query,len(tweets)))


	# picking positive tweets from tweets
	ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']




	# percentage of positive tweets
	print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
	# picking negative tweets from tweets
	ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
	# percentage of negative tweets
	print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))



	#converting in dataframe to sort it by score
	df_pos = pd.DataFrame(ptweets)

	#dataframe with positive tweets
	df_pos_sort = df_pos.sort_values(['score'], ascending=[False])

	#dataframe with negative tweets
	df_neg = pd.DataFrame(ntweets)
	df_neg_sort = df_neg.sort_values(['score'], ascending=[True])

	#print df_neg_sort.head()
	pd.set_option('display.max_colwidth',-1)
		
		

	#printing pos tweets
	print("\n\nPositive tweets:")
	print df_pos_sort.head()
		
	#printing neg tweets
	print("\n\nNegative tweets:")
	print df_neg_sort.head()









	
					
				


 
#username for color run: annenacurtss
