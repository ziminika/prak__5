s = input()
i = 0
substr = ""
while i < len(s):
	substr += s[i]
	if s.count(substr) * len(substr) == len(s):
		num_of_rep = s.count(substr)
		break	
	i += 1
print(num_of_rep)