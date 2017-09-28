import re

with open("mbox-short.txt", "r") as f:
	f = f.readlines()
	for line in f:
		if re.search('From', line):
			print(line)
			num = re.findall('[0-9]+', line)
			print(num)
			name = re.findall('(\S*)@', line)
			print(name)

"""import re

doc = open("mbox-short.txt")
for line in doc:
	line = line.rstrip()
	if re.search('From', line):
		print(line)
		num = re.findall('[0-9]+',line)
		print(num)"""

