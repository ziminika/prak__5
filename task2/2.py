import sys
from collections import defaultdict
end = 0
D = defaultdict(int) 
while end == 0:
	str1 = sys.stdin.readline()
	if str1 != "\n":
		for word in str1[0:-1].split():
			D[word] += 1	
	else:
		end = 1
if D:
	max1 = max(D, key = D.get)
	rez = D[max1]
	D.pop(max1)
	if D:
		max2 = max(D, key = D.get)
		if D[max2] == rez:
			print("-")
		else:
			print(max1)
	else:
		print(max1)
else:
	print("-")