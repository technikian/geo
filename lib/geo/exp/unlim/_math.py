# includes
# none


def cmp(a, b):
	"""compare two arrays, if they are of different length, trailing 0's will be ignored
	little endian byte order"""
	a_i = 0
	for x, y in zip(a, b):
		if x != y:
			return False
		a_i += 1
	b_i = a_i
	while a_i != len(a):
		if a[a_i]:
			return False
		a_i += 1
	while b_i != len(b):
		if b[b_i]:
			return False
		b_i += 1
	return True


def div_value(source, target, value):
	"""divide array of bytes by an integer value, returns remainder
	monstrously slow, only useful for handling large numbers stored as arrays
	source and target may be the same array
	source and target should be of the same length
	little endian byte order"""

	idx = len(source)
	rem = 0
	while idx:
		idx -= 1
		tmp = source[idx]
		tmp += rem << 8
		rem = tmp % value
		target[idx] = tmp // value

	return rem  # returns remainder


def mul_value(source, target, value):

	# todo this probably can't handle large source arrays without exceeding a 64 bit remainder

	idx = 0
	rem = 0
	while idx != len(source):
		tmp = source[idx] * value
		tmp += rem
		rem = tmp >> 8

		if idx != len(target):
			target[idx] = tmp & 0xff
		else:
			target.append(tmp & 0xff)
		idx += 1

	while rem:
		if idx != len(target):
			target[idx] = rem & 0xff
		else:
			target.append(rem & 0xff)
		rem >>= 8
		idx += 1

	return


def add_value(source, target, value):

	idx = 0
	while value:
		value += source[idx]

		if idx != len(target):
			target[idx] = value & 0xff
		else:
			target.append(value & 0xff)

		value >>= 8
		idx += 1

	return


def sub_value():
	pass
