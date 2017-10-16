__author__ = 'adnan'

# To run this code, first edit config.py with your configuration, then:

import sys
import string
import time
import config
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener




class CustomListener(StreamListener):
    """Custom StreamListener for streaming data."""

    def __init__(self, fname):
        safe_fname = format_filename(fname)
	self.outfile = "stream_%s.jsonl" % safe_fname


    def on_data(self, data):
        try:
            with open(self.outfile, 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
		sys.stderr.write("Error on_data: {} \n".format(e))
		time.sleep(5)
        return True

    def on_error(self, status):
        if status ==420:
		sys.stderr.write("Rate limit exceeded\n")
		return False
	else:
		sys.stderr.write("Error {} \n".format(status))
       		return True


def format_filename(fname):
    """Convert file name into a safe string.
    Arguments:
        fname -- the file name to convert
    Return:
        String -- converted file name
    """
    return ''.join(convert_valid(one_char) for one_char in fname)


def convert_valid(one_char):
    """Convert a character into '_' if invalid.
    Arguments:
        one_char -- the char to convert
    Return:
        Character -- converted char
    """
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    if one_char in valid_chars:
        return one_char
    else:
        return '_'


if __name__ == '__main__':

    query = sys.argv[1:]
    query_fname = ' '.join(query)
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)
    twitter_stream = Stream(auth, CustomListener(query_fname))
    twitter_stream.filter(track=query, async=True)
    sys.exit(0)
