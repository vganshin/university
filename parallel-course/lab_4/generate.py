#!/usr/local/bin/python3

from random import randint
import sys

vertex_num = int(sys.argv[1])
edge_num = int(sys.argv[2])

with open('in.txt', 'w') as f:
	f.write('{} {}\n'.format(vertex_num, edge_num))

	for _ in range(edge_num):
		f.write('{} {} {}\n'.format(randint(0, vertex_num - 1), randint(0, vertex_num - 1), randint(1, 10)))


# print(vertex_num, edge_num)