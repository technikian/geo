# includes
from ._math import cmp
from ._math import div_value


def value(source, length=-1):
	"""convert array of bytes to integer value, shouldn't work with sources greater than 8 bytes"""

	target = 0
	shift = 0
	for index, value in enumerate(source):
		if index == length:
			break
		target |= value << shift
		shift += 8

	return target


def string(source, base=10, endian=1, charset=ext.charset.table.dec.gen):
	"""convert bytes source to string representation of specified base
	optional endian and charset (default big endian, decimal charset
	base must not exceed characters in the selected charset"""

	# copy so as not to overwrite mutable object
	source = bytearray(source)

	# convert
	tgt = ""
	zero = 0,
	while not cmp(source, zero):
		rem = div_value(source, source, base)
		tgt += charset.value(rem)

	# reverse if big endian
	if endian:
		rev = ""
		for c in reversed(tgt):
			rev += c
		tgt = rev

	return tgt
