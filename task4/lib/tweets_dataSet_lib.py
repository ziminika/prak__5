import pandas as pd
from collections import Counter
from collections import defaultdict
import re
from pycorenlp import StanfordCoreNLP
import os

nlp = StanfordCoreNLP('http://localhost:9000')

# This function returns a dictionary:
# 	key WORD: a list of the 10 most common words (sorted)
# 	key REITERATION: a list of the number of repetitions of the corresponding words
def top_words(self):
	str_tweets = ""
	result = {}
	for i in self['Tweet content']:
		str_tweets += str(i) + " "
	cnt = Counter(x for x in str_tweets.split())
	index = 1
	result['WORD'] = []
	result['REITERATION'] = []
	for i in cnt.most_common(10):
		result['WORD'].append(i[0])
		result['REITERATION'].append(i[1])
		index += 1
	return result

# This function returns a dictionary:
# 	key TWEET-ID: a list of the 10 most popular tweets (sorted)
# 	key RETWEETED: a list of the retweets of the corresponding tweets
# 	key AUTHOR: a list of the authors of the corresponding tweets 	
def popular_tweets(self):
	tweets = {}
	result = {}
	for i in range(len(self['RTs'])):
		if str(self['RTs'][i]) != 'nan':
			tweets[i] = int(self['RTs'][i])
	list_tweets = list(tweets.items())
	list_tweets.sort(key=lambda i: i[1], reverse=True)
	result['TWEET ID'] = []
	result['RETWEETED'] = []
	result['AUTHOR'] = []
	for i in list_tweets[:10]:
		result['TWEET ID'].append(self['Tweet Id'][i[0]])
		result['RETWEETED'].append(i[1])
		result['AUTHOR'].append(self['User Name'][i[0]])
	return result

# This function returns a dictionary:
# 	key AUTHOR: a list of the 10 most popular authors 	
# 	key FOLLOWERS: a list of the followers of the corresponding authors 	
def popular_authors(self):
	authors = {}
	result = {}
	for i in range(len(self['Followers'])):
		if str(self['Followers'][i]) != 'nan':
			authors[self['User Name'][i]] = int(self['Followers'][i])
	list_authors = list(authors.items())
	list_authors.sort(key=lambda i: i[1], reverse=True)
	result['AUTHOR'] = []
	result['FOLLOWERS'] = []
	for i in list_authors[:10]:
		result['AUTHOR'].append(i[0])
		result['FOLLOWERS'].append(i[1])
	return result

# This function returns a list of dictionaries:
#	 1 dict:
# 		key COUNTRY: a list of 10 countries where people tweet the most
# 		key NUM OF TWEETS: a list of the number of tweets of the corresponding countries
#	 2 dict:
# 		key COUNTRY: a list of 10 countries where people retweet the most
# 		key NUM OF RETWEETS: a list of the number of retweets of the corresponding countries
def top_country(self):
	top_list = [{}, {}]
	country_tweets = defaultdict(int)
	country_retweets = defaultdict(int)
	for i in range(len(self['Tweet content'])):
		if str(self['Country'][i]) != 'nan':
			if str(self['Tweet content'][i]).find('RT @') != -1:
				country_retweets[self['Country'][i]] += 1
			else:
				country_tweets[self['Country'][i]] += 1
	list_country_tweets = list(country_tweets.items())
	list_country_tweets.sort(key=lambda i: i[1], reverse=True)
	top_list[0]['COUNTRY'] = []
	top_list[0]['NUM OF TWEETS'] = []
	for i in list_country_tweets[:10]:
		top_list[0]['COUNTRY'].append(i[0])
		top_list[0]['NUM OF TWEETS'].append(i[1])
	list_country_retweets = list(country_retweets.items())
	list_country_retweets.sort(key=lambda i: i[1], reverse=True)
	top_list[1]['COUNTRY'] = []
	top_list[1]['NUM OF RETWEETS'] = []
	for i in list_country_retweets[:10]:
		top_list[1]['COUNTRY'].append(i[0])
		top_list[1]['NUM OF RETWEETS'].append(i[1])
	return top_list

# This function returns a dictionary:
# 	key TWEET ID: a list of the tweets
# 	key RESULT NER: a list of the results of the algorithm NLP with each Tweet content
def NLP(self):
	dictionary = {}
	dictionary['TWEET ID'] = []
	dictionary['RESULT NER'] = []
	for i in range(len(self['Tweet content'])):
		analysis = str(self['Tweet content'][i])
		pos = []
		result = nlp.annotate(analysis, properties={'annotators': 'ner', 'outputFormat': 'json', 'timeout': 1500000 })
		for word in result["sentences"][0]['tokens']:
			pos.append('{} ({})'.format(word['word'], word['ner']))
		dictionary['TWEET ID'].append(self['Tweet Id'][i])
		dictionary['RESULT NER'].append(" ".join(pos))
	return dictionary