import re
import tweepy
import os
from tweepy import OAuthHandler
from textblob import TextBlob
import sys
import json
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import operator
import pandas as pd
from tabulate import tabulate
import string
from collections import Counter
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords

class TwitterClient(object):
	'''
	Generic Twitter Class for sentiment analysis.
	'''

	def clean_tweet(self, tweet):
		'''
		Utility function to clean tweet text by removing links, special characters
		using simple regex statements.
		'''
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

	def get_tweet_sentiment(self, tweet):
		'''
		Utility function to classify sentiment of passed tweet
		using textblob's sentiment method
		'''
		# create TextBlob object of passed tweet text
		analysis = TextBlob(self.clean_tweet(tweet))
		# set sentiment
		if analysis.sentiment.polarity > 0:
			return 'positive'
		elif analysis.sentiment.polarity == 0:
			return 'neutral'
		else:
			return 'negative'



	def get_tweet_polarity_score(self, tweet):
		'''
		Utility function to get polarity score from tweets
		'''
		# create TextBlob object of passed tweet text
		analysis = TextBlob(self.clean_tweet(tweet))
		return analysis.sentiment.polarity


	def get_tweets(self,fname):
		'''
		Main function to fetch tweets and parse them.
		'''
		# empty list to store parsed tweets
		tweets = []

		try:

			
			with open(fname, 'r') as f:
				for line in f:
					tweet = json.loads(line)




 # empty dictionary to store required params of a tweet
					parsed_tweet = {}

					# saving text of tweet
					parsed_tweet['text'] = tweet['text']
					# saving sentiment of tweet
					parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet['text'])
					# saving ploarity score of tweet
					parsed_tweet['score'] = self.get_tweet_polarity_score(tweet['text'])

					# appending parsed tweet to tweets list
					if tweet['retweet_count'] > 0:
						# if tweet has retweets, ensure that it is appended only once
						if parsed_tweet not in tweets:
							tweets.append(parsed_tweet)
					else:
						tweets.append(parsed_tweet)

				# return parsed tweets
			return tweets

		except tweepy.TweepError as e:
			# print error (if any)
			print("Error : " + str(e))




def process (text, tokenizer=TweetTokenizer(), stopwords=[]):
	text= text.lower()
	tokens = tokenizer.tokenize(text)
	return [tok for tok in tokens if tok not in stopwords and not tok.isdigit()]


def print_most_freq(tweets):
	tf = Counter()
	tweet_tokenizer = TweetTokenizer()
	punct = list(string.punctuation)
	stopword_list = stopwords.words('english')+punct+['rt','via','...']

	for i in range(len(tweets)):
		tokens = process(text=tweets[i]['text'],tokenizer=tweet_tokenizer, stopwords=stopword_list)
		tf.update(tokens)
	for tag, count in tf.most_common(20):
		print("{} : {} ".format(tag.encode('utf-8'), count))	
	




def main(fname):

		# creating object of TwitterClient Class
		api = TwitterClient()

		# calling function to get tweets
		tweets = api.get_tweets(fname)
		print len(tweets)


		# picking positive tweets from tweets
		ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
		ptweets_percentage = 100*len(ptweets)/len(tweets)




		# percentage of positive tweets
		print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
		# picking negative tweets from tweets
		ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']



		ntweets_percentage = 100*len(ntweets)/len(tweets)

		neutral_percentage = 100 - ptweets_percentage -ntweets_percentage







		
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




		#most frequent words in positive tweets
		print("\n\nMost frequent words in Positive tweets:")
		print_most_freq(ptweets)

		#most frequent words in negative tweets
		print("\n\nMost frequent words in Negative tweets:")
		print_most_freq(ntweets)

		#code for barchart
		percentages = [ptweets_percentage, ntweets_percentage, neutral_percentage]
		objects = ('positive tweet (%)', 'negative tweets (%)', 'neutral tweets (%)')
		y_pos = np.arange(len(objects))
		bar_width = 0.7

		plt.bar(y_pos, percentages, align='center', alpha=0.8)

		plt.xticks(y_pos, objects)
		#plt.ylim(0,0)
		plt.ylabel('Percentage')
		plt.title('Sentiment analysis')

		plt.show()

if __name__ == "__main__":
	# calling main function
	fname = sys.argv[1]
	main(fname)

