# from . import typewise


def lowest_set_bit(value):
	shift = 0
	while not value & 1 << shift:
		shift += 1
	return shift


def highest_power_2(value):
	mask = 1
	while mask < value:
		mask <<= 1
	return mask >> 1


def pow(a, e):
	print(a**e)
	hpt = highest_power_2(a)
	lsb = lowest_set_bit(hpt)
	tgt = (1 << (lsb * e)) * (a / hpt) ** e
	print(tgt)


# powers method (power of a
# divide by the highest power of 2 that is not greater than a
# let x = highest power
# let y = a / x  ( this will never be greater than 2)
# so a = xy
# kind of works, need a better way to take exponent of (a / hpt)


# addition overflow of two integers
def add(max, a, *args):
	"""check for the addition overflow of integers a and b, when a + b > max"""
	if len(args) == 1:
		return a > 0 and args[0] > max - a
	ovr = 0
	for arg in args:
		ovr += a > 0 and arg > max - a
		a += arg
	return ovr



