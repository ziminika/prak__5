import socket
from multiprocessing import Process
import pickle
from collections import Counter
from collections import defaultdict
import re
from pycorenlp import StanfordCoreNLP
import pandas as pd
import os
from lib import tweets_dataSet_lib as tl

N = 5 # maximum number of connections

# send of the file
def send_file(sock, df):
	msg = pickle.dumps(df)
	size = len(msg)
	inf = str(size)
	sock.send(inf.encode('utf-8'))
	sock.recv(1024)
	sock.send(msg)
	sock.recv(1024)
	
# This function collects statistics and sends tables to the client	
def stat(self, size):
	self.send("STAT".encode("utf-8"))
	sizeof = int(size)
	data = b""
	while sizeof - 4096 > 0:
		packet = self.recv(4096)
		if not packet:
			break
		data += packet
		sizeof -= 4096
	packet = self.recv(sizeof)
	data += packet
	data_arr = pickle.loads(data)

	df = pd.DataFrame(tl.top_words(data_arr))
	df.to_csv(index=False)
	send_file(self, df)

	df = pd.DataFrame(tl.popular_tweets(data_arr))
	df.to_csv(index=False)
	send_file(self, df)

	df = pd.DataFrame(tl.popular_authors(data_arr))
	df.to_csv(index=False)
	send_file(self, df)

	list_tw_and_rt = tl.top_country(data_arr)
	df_tweets = pd.DataFrame(list_tw_and_rt[0])
	df_retweets = pd.DataFrame(list_tw_and_rt[1])
	df_tweets.to_csv(index=False)
	send_file(self, df_tweets)
	df_retweets.to_csv(index=False)
	send_file(self, df_retweets)

# This function applies the NER algorithm and sends the table to the client
def enti(self, size):
	self.send("ENTI".encode("utf-8"))
	sizeof = int(size)
	data = b""
	while sizeof - 4096 > 0:
		packet = self.recv(4096)
		if not packet:
			break
		data += packet
		sizeof -= 4096
	packet = self.recv(sizeof)
	data += packet
	data_arr = pickle.loads(data)
	df = pd.DataFrame(tl.NLP(data_arr))
	df.to_csv(index=False)
	send_file(self, df)
	
# This function analyzes the query mode and starts the required function
def handler(conn):
	data = conn.recv(1024)
	if not data:	
		return
	size = data.decode("utf-8").split(' ')[1]
	if data.decode("utf-8").split(' ')[0] == 'STAT':
		stat(conn, size)
	else:
		enti(conn, size)
	conn.close()

if __name__ == '__main__':
	sock = socket.socket()
	sock.bind(('', 9081))
	sock.listen(N)
	while True:
		conn, addr = sock.accept()
		print('connected:', addr)
		p = Process(target=handler, args=(conn,))
		p.start()
	sock.close()
