import numpy as np
from functools import reduce

a = []
b = []
x_prev = []
x = []

with open('in.txt') as f:
    n, eps = f.readline().split(' ')
    n = int(n)
    eps = float(eps)
    for i in range(n):
        line = f.readline().split(' ')
        _a = []
        for j in range(n):
            _a.append(float(line[j]))
        a.append(_a)
        b.append(float(line[n]))

with open('out.txt') as f:
	answer = [float(v) for v in f.readline().split(' ')[:n]]

right_answer = np.linalg.solve(a,b)

# print(right_answer)
# print(answer)

if reduce(lambda a, b: a if a > b else b, list(right_answer - answer)) > eps:
	print("Error")
	exit(1)

print("OK")
