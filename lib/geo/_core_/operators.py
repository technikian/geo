
from copy import deepcopy as _deepcopy


class Compare:
	"""
	inheritable object, giving child the properties of the boolean operators
	"""

	#
	# required - override these
	#

	# <
	def __lt__(self, other):
		pass

	#
	# defaults - override these to improve performance
	#

	# ==
	def __eq__(self, other):
		return not self < other and not other < self

	#
	# dependent - automatically implemented based off the == and < implementation
	#

	# !=
	def __ne__(self, other):
		return not self == other

	# >
	def __gt__(self, other):
		return other < self

	# <=
	def __le__(self, other):
		# return not self > other
		return not other < self

	# >-
	def __ge__(self, other):
		return not self < other


class Bitwise:
	pass


class Derived:

	def __zero__(self):
		return _deepcopy(self).__isub__(self)

	#
	# required - you must override these
	#

	# +=
	def __iadd__(self, other):
		pass

	# -=
	def __isub__(self, other):
		pass

	# &=
	def __iand__(self, other):
		pass

	# |=
	def __ior__(self, other):
		pass

	# ^=
	def __ixor__(self, other):
		pass

	# /=
	def __itruediv__(self, other):
		pass

	#
	# defaults - override these to improve performance
	#

	# *=
	def __imul__(self, other):
		temp = self
		i = 0
		while i < other:
			self.__iadd__(temp)
			i += 1
		return self

	# **=
	def __ipow__(self, other):
		temp = self
		i = 0
		while i < other:
			self.__imul__(temp)
			i += 1
		return self

	# # /=
	# def __itruediv__(self, other):
	# 	pass

	# //=
	def __ifloordiv__(self, other):
		pass

	# %=
	def __imod__(self, other):
		pass

	# # +=
	# def __iadd__(self, other):
	# 	pass

	# # -=
	# def __isub__(self, other):
	# 	pass

	# # &=
	# def __iand__(self, other):
	# 	pass

	# # |=
	# def __ior__(self, other):
	# 	pass

	# # ^=
	# def __ixor__(self, other):
	# 	pass

	# <<=
	def __ilshift__(self, other):
		pass

	# >>=
	def __irshift__(self, other):
		pass

	# ~ operator
	def __invert__(self):
		return -self - 1

	# - operator
	def __neg__(self):
		return self.__zero__().__isub__(self)

	# absolute value
	def __abs__(self):
		pass

	#
	# dependent
	#

	def __mul__(self, other):
		# return self.value.__mul__(other)
		return _deepcopy(self).__imul__(other)

	def __pow__(self, power, modulo=None):
		# return self.value.__pow__(power, modulo)
		return _deepcopy(self).__ipow__(power)

	def __truediv__(self, other):
		# return self.value.__truediv__(other)
		return _deepcopy(self).__itruediv__(other)

	def __floordiv__(self, other):
		# return self.value.__floordiv__(other)
		return _deepcopy(self).__ifloordiv__(other)

	def __mod__(self, other):
		# return self.value.__mod__(other)
		return _deepcopy(self).__imod__(other)

	def __add__(self, other):
		# return self.value.__add__(other)
		return _deepcopy(self).__iadd__(other)

	def __sub__(self, other):
		# return self.value.__sub__(other)
		return _deepcopy(self).__isub__(other)

	def __and__(self, other):
		# return self.value.__and__(other)
		return _deepcopy(self).__iand__(other)

	def __or__(self, other):
		# return self.value.__or__(other)
		return _deepcopy(self).__ior__(other)

	def __xor__(self, other):
		# return self.value.__xor__(other)
		return _deepcopy(self).__ixor__(other)

	def __lshift__(self, other):
		# return self.value.__lshift__(other)
		return _deepcopy(self).__ilshift__(other)

	def __rshift__(self, other):
		# return self.value.__rshift__(other)
		return _deepcopy(self).__irshift__(other)

	def __divmod__(self, other):
		return self // other, self % other

	# end
