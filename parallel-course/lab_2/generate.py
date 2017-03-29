from random import random
import sys

n = int(sys.argv[1])
eps = float(sys.argv[2])

a = []

for i in range(n):
	_a = []
	s = 0
	for j in range(n):
		if i != j:
			tmp = random()*100
			_a.append(tmp)
			s = s + tmp
	_a.insert(i, s + random()*100)
	_a.append(random()*1000)
	a.append(_a)

with open('in.txt', 'w') as f:
	f.write('{n} {eps}\n'.format(n=n, eps=eps))
	f.write('\n'.join([' '.join([str(v) for v in _a]) for _a in a]))