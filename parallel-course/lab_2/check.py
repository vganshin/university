a = []
b = []
x_prev = []
x = []


def check():
    d = []
    for i in range(n):
        d.append(a[i * n + i])


with open('in.txt') as f:
    n = int(f.readline())
    for i in range(n):
        line = f.readline().split(' ')
        _a = []
        for j in range(n):
            _a.append(float(line[j]))
        a.append(_a)
        b.append(float(line[n]))

import numpy as np

answer = np.linalg.solve(a,b)


for i in range(n):
	tmp = 0
	for j in range(n):
		tmp = tmp + a[i][j] * answer[j]
	print(tmp)



# for i in range(n):
#     x_prev.append(b[i] / a[i * n + i])

# print("x_0 ", x_prev)

# for i in range(n):
#     tmp = b[i]
#     for j in range(n):
#         if i != j:
#             tmp -= a[i * n + j] * x_prev[j]
#     tmp /= a[i * n + i]
#     x.append(tmp)


# print(x)

# k = 0
# norm = 1
# # old = [x_prev]

# while norm > 0.001:
#     for i in range(n):
#         tmp = b[i]
#         for j in range(n):
#             if i != j:
#                 tmp -= a[i * n + j] * x_prev[j]
#         tmp /= a[i * n + i]
#         x.append(tmp)

#     norm = abs(x_prev[0] - x[0])
#     for i in range(n):
#         if abs(x_prev[i] - x[i]) > norm:
#             norm = abs(x_prev[i] - x[i])
#     # old.append(x)
#     x_prev = x
#     x = []
#     k += 1

# for i in range(n):
#     tmp = 0
#     for j in range(n):
#         tmp += a[i * n + j] * x_prev[j]
#     print(0.01 > abs(b[i] - tmp), tmp, abs(b[i] - tmp))