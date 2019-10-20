import librosa
import numpy as np
import os
import time
import sys
import warnings
from concurrent.futures import ProcessPoolExecutor, as_completed

warnings.filterwarnings('ignore')

def mfcc_search(input_dir, output_dir):
	for address, dirs, files in os.walk(input_dir):
		if not os.path.exists(output_dir + "/" + address):
			os.makedirs(output_dir + '/' + address)
		for file in files:
			y, sr = librosa.load(address + '/' + file)
			mfcc = librosa.feature.mfcc(y=y, sr=sr)
			np.save(output_dir + "/" + address + '/' + file[:-4], mfcc)

if __name__ == "__main__":
	if (len(sys.argv) < 2):
		print("Input error: No input dir entered")
	else:
		input_dir = sys.argv[1]
		output_dir = "res_proc" # default output dir
		if (len(sys.argv) >= 3):
			output_dir = sys.argv[2]
		
		start_time = time.time()

		with ProcessPoolExecutor(max_workers=4) as pool:
			pool.submit(mfcc_search, input_dir, output_dir)

		print("--- %s seconds ---" % (time.time() - start_time))