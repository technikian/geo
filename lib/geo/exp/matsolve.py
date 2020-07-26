
from lib.geo.tensor._type_ import SubscriptableGenerator
from lib.geo.matrix import Matrix


def solve(coefficients, constants):
	"""coefficients: x*x matrix of equation coefficients, constants: x*1 matrix of the equation constants"""
	inv_coeff = Matrix.from_tensor(~coefficients)
	r = inv_coeff * constants
	return Matrix.from_tensor(r)


def line_intersect(ax, ay, bx, by, cx, cy, dx, dy):
	def solve(coefficients, constants):
		"""coefficients: x*x matrix of equation coefficients, constants: x*1 matrix of the equation constants"""
		inv_coeff = Matrix.from_tensor(~coefficients)
		r = inv_coeff * constants
		return Matrix.from_tensor(r)
	abx = bx - ax
	aby = by - ay
	cdx, cdy = dx - cx, dy - cy
	coefficients = Matrix(2, 2, (abx, -cdx, aby, -cdy))
	constants = Matrix(2, 1, (cx - ax, cy - ay))
	try:
		r = solve(coefficients, constants)
	except ZeroDivisionError:
		# print("warning: check inputs", ax, ay, bx, by, cx, cy, dx, dy)
		return None, None
	return (ax + r[0, 0] * abx, ay + r[0, 0] * aby) if 0 <= r[0, 0] <= 1 and 0 <= r[1, 0] <= 1 else (None, None)


if __name__ == "__main__":
	print(solve(Matrix(2, 2, (1, 2, 3, -5)), Matrix(2, 1, (4, 1))))
	# print(solve(Matrix(2, 2, (0, 0, 0, 6)), Matrix(2, 1, (0, 3))))
	print(line_intersect(0, 0, 5, 5, 2, -1, 2, 5))
