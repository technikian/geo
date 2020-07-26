
from geo.matrix import Matrix
from geo import Expression as Expr

a = Matrix(1, 3, (2, 3, 4))
b = Matrix(3, 1, (1, 1, 1))
c = a * b

print(a)
print(b)
print(c)
# print(matrix.to_str(c))


if __name__ == "__main__":
	z = Expr(None, 2)
	a = Expr(None, 8)
	a += 2
	b = a + 2 - z + z * 3
	c = b.eval()
	print(c, b)
