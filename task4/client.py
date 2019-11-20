import socket
from pandas import read_csv
import pandas as pd
import os
import pickle
import time

# this function returns the DataFrame of the first number of tweets from the entered file
def crop_file(file, number):
	new_file = {}
	for rows in file:
		new_file[rows] = []
		index = number
		for value in file[rows]:
			new_file[rows].append(value)
			index -= 1
			if index == 0:
				break
	return(pd.DataFrame(new_file))

# presentation of results
output_dir = r'result/'
f_words = output_dir + r"top_words.csv"
f_authors = output_dir + r"popular_authors.csv"
f_tweets = output_dir + r"top_tweets.csv"
f_country_tweets = output_dir + r"top_country_tweets.csv"
f_country_retweets = output_dir + r"top_country_retweets.csv"
list_of_files = [f_words, f_tweets, f_authors, f_country_tweets, f_country_retweets]
f_nlp = output_dir + r"nlp_result.csv"

# getting the result from the server
def recv_file(sock):
	data = sock.recv(1024)
	size = data.decode("utf-8")
	sock.send("ready".encode('utf-8'))
	sizeof = int(size)
	data = b""
	while sizeof - 4096 > 0:
		packet = sock.recv(4096)
		if not packet:
			break
		data += packet
		sizeof -= 4096
	packet = sock.recv(sizeof)
	data += packet
	data_arr = pickle.loads(data)
	sock.send("end".encode('utf-8'))
	return data_arr

# input and verification of the correctness of initial 
# information: file name for analysis and mode 
print("Enter filename: ", end='')
filename = input()
if filename.rfind('.csv') == -1:
	print('Error: Invalid file format')
	exit(1)
try:
	file = pd.read_csv(filename, sep=';', encoding='ISO8859-1')
except FileNotFoundError:
	print('Error: File doesn\'t exists')
	exit(1)
print("Enter mode: (STAT or ENTI): ", end='')
mode = input().lower()
if  mode != 'stat' and mode != 'enti':
	print('Error: Incorrect operating mode')
	exit(1)
print("Enter number of tweets: ", end='')
number = int(input())

# sending a file to the server
sock = socket.socket()
sock.connect(('localhost', 9081))
msg = pickle.dumps(crop_file(file, number))
size = len(msg) 
inf = mode.upper() + " " + str(size)
sock.send(inf.encode('utf-8'))
data = sock.recv(1024)
sock.send(msg)

# reception of results. The result is represented by a files in output_dir: 
if not os.path.exists(output_dir):
	os.makedirs(output_dir)
if mode.upper() == "STAT":
	for i in list_of_files:
		df = recv_file(sock)
		df.to_csv(i, index=False)
else:
	df = recv_file(sock)
	df.to_csv(f_nlp, index=False)
sock.close()

