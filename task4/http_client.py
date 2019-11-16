import requests
from pandas import read_csv
import pandas as pd
import pickle

# server url
url = 'http://0.0.0.0:8000/'

sep = " ********** "

# input and verification of the correctness of initial 
# information: file name for analysis and mode 
print("Enter filename: ", end='')
filename = input()
if filename.rfind('.csv') == -1:
	print('Error: Invalid file format')
	exit(1)
try:
	file = pd.read_csv(filename, sep=';')
except FileNotFoundError:
	print('Error: File doesn\'t exists')
	exit(1)
print("Enter mode: (STAT or ENTI): ", end='')
mode = input().lower()
if  mode != 'stat' and mode != 'enti':
	print('Error: Incorrect operating mode')
	exit(1)

# sending a file to the server
msg = pickle.dumps(file)
r = requests.post(url + mode, data=msg)

# reception of results. The result is represented by a table dictionary: 
# key - table name; value - table
result = pickle.loads(r.content)
for table_name in result:
	print('\n', sep, table_name, sep)
	print(result[table_name])