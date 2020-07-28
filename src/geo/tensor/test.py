from src.tensor import Tensor


if __name__ == "__main__":
	# t = Tensor((3, 3), (1,2,3,4,5,6,7,8,9))
	t = Tensor((3, 2), (1, 2, 3, 4, 5, 6))
	print(t[0, 1])
	print(t[1, 1])
	# print(t[2, 1])

	# 1, 4, 7
	# 2, 5, 8
	# 3, 6, 9

	# V(1, 2, 3)
	# V(4, 5, 6)

	print(t.dimension(None, 1).values)
	print(t.steps)

	print()
	# print(len(t[0]))
	print(t[1][0])
	print(t[1][1])
	print(t[1][2])

	print()

	for row in reversed(t):
		for col in reversed(row):
			print(col)

	print()
	u = ((1, 2, 3), (4, 5, 6))
	for row in reversed(u):
		for col in reversed(row):
			print(col)
