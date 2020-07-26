# includes
from ._math import mul_value
from ._math import add_value


def value(source):
	"""convert integer value to array of bytes, shouldn't work with sources greater than 8 bytes"""

	target = bytearray()
	while source:
		target.append(source & 0xff)
		source >>= 8

	return target


def string(source, base=10, endian=1, charset=ext.charset.table.dec.gen):
	"""convert string representation to array using specified base
	optional endian and charset (default big endian, decimal charset
	base must not exceed characters in the selected charset"""

	# reverse if little endian
	itr = iter(source) if endian else reversed(source)

	# convert
	tgt = bytearray([0])
	for c in itr:
		mul_value(tgt, tgt, base)
		add_value(tgt, tgt, charset.index(c))

	return tgt
