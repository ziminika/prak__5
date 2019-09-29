from itertools import product
num = input()
x = []
result = []
s = {2: 'abc', 3: 'def', 4: 'ghi', 5: 'jkl', 6: 'mno', 7: 'pqrs', 8: 'tuv', 9: 'wxyz'}
for i in num:
	if int(i) in s:
		x.append(s[int(i)])
for item in (product(*x)):
    result.append(''.join(item))
print("[" + '\"'.join(result) + "]")