from geo import Matrix
from random import randint

if __name__ == "__main__":
	pass

# m = Matrix(3, 3, (1, 2, 3, 4, 5, 6, 7, 8, 9))
m = Matrix(3, 3, tuple(randint(-100, 100) for i in range(9)))
print(m)
print(m.transpose().transpose())
print(m._determinant_3())
print(m.transpose()._determinant_3())
