# SentimentAnalysis
It contains 3 programs. In order to run any program, you first need to put your own credentials in config.py file.

user_timeline_sentiment_updated.py
1) This program is based on Twitter Rest api. In order to execute it from command shell, enter the following command.

$ python user_timeline_sentiment_updated.py username \#tag1

2) It will go on the username's timeline and read tweets (up to 3200 tweets), filter it according to i/p hashtag and apply sentiment analysis to provide if a user has positive or negative view about that hashtag. It also sort the most positive and negative tweets of the user,and display it. 


twitter_streaming.py
1) This program is based on Twitter streaming api to ingest tweets in real-time based on the i.p filter.  In order to run it,

$ python twitter_streaming.py \#tag1 \#tag2

2) It will start ingesting tweets in real-time based on the i/p filter and will save it in the json format.


twitter_sentiment.py
1) This program needs i/p file (saved from the twitter_streaming.py) and applies sentiment analysis on it to detect if the people are having a positive review or negative review about specific event

2) It also sorts the tweets and displays most positive and negative tweets. It can be used by event organizers to get feedback about their event in real-time and based on negative tweets they can address it in real-time to improve users experience. 
