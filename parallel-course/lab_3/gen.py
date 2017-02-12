from random import randint
import sys

len = int(sys.argv[1])

with open('in.txt', 'w') as file:
	file.write(str(len) + '\n')
	file.write(' '.join([str(randint(1, 100)) for _ in range(len)]))