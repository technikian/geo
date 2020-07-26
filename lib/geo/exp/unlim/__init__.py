# title
"""unlimited integer module
little endian byte order!"""


# includes
from ._math import *
from . import fr
from . import to


class Unlim8:
	def __init__(self, value):
		pass


# is an iterable
class Unlim:
	def __init__(self, value, subtype=int, submask=0xff, container=list):
		self._cont = container()

	def size(self):
		return self._cont.__len__()
