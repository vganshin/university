from random import random
import sys
import math

a_row = int(sys.argv[1])
b_row = a_column = int(sys.argv[2])
b_column = int(sys.argv[3])

a = open("a.txt", "w")
b = open("b.txt", "w")


def gen_matrix(row, column):

    matrix = []

    for i in range(row):
        matrix.append([])
        for j in range(column):
            # matrix[i].append(str(int(math.floor(random()*10))))
            matrix[i].append("1")

    return matrix


a.write("{} {}\n".format(a_row, a_column))
a.write("\n".join([" ".join(m) for m in gen_matrix(a_row, a_column)]))
a.close()

b.write("{} {}\n".format(b_row, b_column))
b.write("\n".join([" ".join(m) for m in gen_matrix(b_row, b_column)]))
b.close()