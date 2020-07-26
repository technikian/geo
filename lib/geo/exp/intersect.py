
from lib.geo.vector import Vector


def intersect(*geometries):
	pass


def interpolate(a, b, x):
	"""a: start point, b: end point, x: scale/ratio factor of (b - a)"""
	delta = b - a  # final - initial
	return x * delta + a


def line_intersect(line_a, line_b):
	pass


if __name__ == "__main__":
	pass

aa = Vector(3, (1, 2, 3))
ab = Vector(3, (1, 2, 5))

ba = Vector(3, (0, 2, 4))
bb = Vector(3, (2, 2, 4))



