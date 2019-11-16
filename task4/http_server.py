from http.server import HTTPServer, BaseHTTPRequestHandler
import pickle
import pandas as pd
from collections import Counter
from collections import defaultdict
import re
from pycorenlp import StanfordCoreNLP
import os
from lib import tweets_dataSet_lib as tl
from multiprocessing import Process

# this function returns the collected statistics as a byte string
# 	The collected statistics are presented by the dictionary: key - table name; value - table
def stat(self):
	result = {}

	df_words = pd.DataFrame(tl.top_words(self))
	df_words.to_csv(index=False)
	result['TOP WORDS'] = df_words

	df_tweets = pd.DataFrame(tl.popular_tweets(self))
	df_tweets.to_csv(index=False) 
	result['TOP TWEETS'] = df_tweets

	df_authors = pd.DataFrame(tl.popular_authors(self))
	df_authors.to_csv(index=False)
	result['POPULAR AUTHORS'] = df_authors

	list_tw_and_rt = tl.top_country(self)
	df_country_tweets = pd.DataFrame(list_tw_and_rt[0])
	df_country_retweets = pd.DataFrame(list_tw_and_rt[1])
	df_country_tweets.to_csv(index=False)
	result['TOP COUNTRY TWEETS'] = df_country_tweets
	df_country_retweets.to_csv(index=False)
	result['TOP COUNTRY RETWEETS'] = df_country_retweets
	return pickle.dumps(result)

# this function returns the result of NLP as a byte string
# 	The result of NLP are presented by the dictionary: key - table name; value - table
def enti(self):
	result = {}
	df = pd.DataFrame(tl.NLP(self))
	df.to_csv(index=False)
	result['NLP NER'] = df
	return pickle.dumps(result)	

class RequestHeandler(BaseHTTPRequestHandler):
	def _set_headers(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()

	def do_GET(self):
		self._set_headers()
		self.wfile.write(self._html("hi!"))

	def do_HEAD(self):
		self._set_headers()

	def do_POST(self):
		content_length = int(self.headers['Content-Length'])
		data = self.rfile.read(content_length)
		data_arr = pickle.loads(data)
		self._set_headers()
		if self.path == '/stat':
			res = stat(data_arr)
		else:
			res = enti(data_arr)
		self.wfile.write(res)

def run(server_class=HTTPServer, handler_class=RequestHeandler, addr="localhost", port=8000):
	server_address = (addr, port)
	httpd = server_class(server_address, handler_class)
	print(f"Starting httpd server on {addr}:{port}")
	httpd.serve_forever()

if __name__ == '__main__':
	run()