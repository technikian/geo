
NOT_DEFINED_DERIVED = "! not defined by derived class"


class ContextManageable:
	def __enter__(self):
		e = self.open()
		if e:
			raise e
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		e = self.close()
		if e:
			raise e

	def open(self):
		raise NotImplementedError(NOT_DEFINED_DERIVED)

	def close(self):
		raise NotImplementedError(NOT_DEFINED_DERIVED)


class Logical:
	pass


class Comparable:
	#
	# required - override these
	#

	# <
	def __lt__(self, other):
		raise NotImplementedError(NOT_DEFINED_DERIVED)

	#
	# defaults - override these to improve performance
	#

	# ==
	def __eq__(self, other):
		return not self < other and not other < self

	#
	# dependent - automatically implemented based off the == and < implementation
	#

	# >
	def __gt__(self, other):
		return other < self

	# !=
	def __ne__(self, other):
		return not self == other

	# <=
	def __le__(self, other):
		return not other < self

	# >-
	def __ge__(self, other):
		return not self < other


class Translatable:
	#
	# required - override these
	#

	def __add__(self, other):
		raise NotImplementedError(NOT_DEFINED_DERIVED)

	def __sub__(self, other):
		raise NotImplementedError(NOT_DEFINED_DERIVED)

	#
	# defaults - override these to improve performance
	#

	def __neg__(self):
		return self - self - self

	#
	# dependent - automatically implemented based off the == and < implementation
	#

	def __iadd__(self, other):
		return self + other

	def __radd__(self, other):
		return self + other

	def __isub__(self, other):
		return self - other

	def __rsub__(self, other):
		return -self + other


class Scalable:
	#
	# required - override these
	#

	def __mul__(self, other):
		raise NotImplementedError(NOT_DEFINED_DERIVED)

	def __truediv__(self, other):
		raise NotImplementedError(NOT_DEFINED_DERIVED)

	def __floordiv__(self, other):
		raise NotImplementedError(NOT_DEFINED_DERIVED)

	#
	# dependent - automatically implemented based off the == and < implementation
	#

	def __imul__(self, other):
		return self * other

	def __rmul__(self, other):
		return self * other  # todo usually commutable, but not always, perhaps raise warning?

	def __itruediv__(self, other):
		return self / other

	def __ifloordiv__(self, other):
		return self // other
