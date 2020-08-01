#
# classes to be inherited from to simplify the creation of classes with common properties
#

# includes
from copy import deepcopy


class Conditional:
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


class Operable:

	def __zero__(self):
		return deepcopy(self).__isub__(self)

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
		return deepcopy(self).__imul__(other)

	def __pow__(self, power, modulo=None):
		# return self.value.__pow__(power, modulo)
		return deepcopy(self).__ipow__(power)

	def __truediv__(self, other):
		# return self.value.__truediv__(other)
		return deepcopy(self).__itruediv__(other)

	def __floordiv__(self, other):
		# return self.value.__floordiv__(other)
		return deepcopy(self).__ifloordiv__(other)

	def __mod__(self, other):
		# return self.value.__mod__(other)
		return deepcopy(self).__imod__(other)

	def __add__(self, other):
		# return self.value.__add__(other)
		return deepcopy(self).__iadd__(other)

	def __sub__(self, other):
		# return self.value.__sub__(other)
		return deepcopy(self).__isub__(other)

	def __and__(self, other):
		# return self.value.__and__(other)
		return deepcopy(self).__iand__(other)

	def __or__(self, other):
		# return self.value.__or__(other)
		return deepcopy(self).__ior__(other)

	def __xor__(self, other):
		# return self.value.__xor__(other)
		return deepcopy(self).__ixor__(other)

	def __lshift__(self, other):
		# return self.value.__lshift__(other)
		return deepcopy(self).__ilshift__(other)

	def __rshift__(self, other):
		# return self.value.__rshift__(other)
		return deepcopy(self).__irshift__(other)

	def __divmod__(self, other):
		return self // other, self % other

	# end


# any commented function means I don't know what it does and it causes some kind of error
# noinspection SpellCheckingInspection
class AutoValue(Conditional, Operable):
	"""inheriting from this class provides math operation functionality based off
	a member "value"

	property "value" must be defined!
	"""

	@property
	def value(self):
		raise AttributeError("can't get attribute: ensure sub class defines @property value")

	@value.setter
	def value(self, x):
		raise AttributeError("can't set attribute: ensure sub class defines @value.setter")

	# def __init__(self):
	# 	pass

	#
	# comparison definitions
	#

	def __eq__(self, other):
		try:
			return self.value == other.value
		except AttributeError:
			return self.value == other

	def __lt__(self, other):
		try:
			return self.value < other.value
		except AttributeError:
			return self.value < other

	#
	# operation definitions
	#

	# *=
	def __imul__(self, other):
		self.value *= other
		return self

	# **=
	def __ipow__(self, other):
		self.value **= other
		return self

	# /=
	def __itruediv__(self, other):
		self.value /= other
		return self

	# //=
	def __ifloordiv__(self, other):
		self.value //= other
		return self

	# %=
	def __imod__(self, other):
		self.value %= other
		return self

	# +=
	def __iadd__(self, other):
		self.value += other
		return self

	# -=
	def __isub__(self, other):
		self.value -= other
		return self

	# &=
	def __iand__(self, other):
		self.value &= other
		return self

	# |=
	def __ior__(self, other):
		self.value |= other
		return self

	# ^=
	def __ixor__(self, other):
		self.value ^= other
		return self

	# <<=
	def __ilshift__(self, other):
		self.value <<= other
		return self

	# >>=
	def __irshift__(self, other):
		self.value >>= other
		return self

	def __invert__(self):
		return ~self.value

	#
	# obscure math operations
	# right side math operations
	#

	def __neg__(self):
		return self.value.__neg__()
		# return 0 - self

	def __abs__(self):
		return self.value.__abs__()
		# return -self if self < 0 else self

	def __ceil__(self):
		return self.value.__ceil__()

	# def __idiv__(self, other):  # depreciated in python 3
	# 	return self.value.__idiv__(other)

	def __floor__(self):
		return self.value.__floor__()

	def __imatmul__(self, other):
		return self.value.__imatmul__(other)
		# matrix multiplication

	def __radd__(self, other):
		return self.value.__radd__(other)

	def __rand__(self, other):
		return self.value.__rand__(other)

	def __rdiv__(self, other):
		return self.value.__rdiv__(other)

	def __rdivmod__(self, other):
		return self.value.__rdivmod__(other)

	def __rfloordiv__(self, other):
		return self.value.__rfloordiv__(other)

	def __rlshift__(self, other):
		return self.value.__rlshift__(other)

	def __rmatmul__(self, other):
		return self.value.__rmatmul__(other)

	def __rmod__(self, other):
		return self.value.__rmod__(other)

	def __rmul__(self, other):
		return self.value.__rmul__(other)

	def __ror__(self, other):
		return self.value.__ror__(other)

	def __rpow__(self, other):
		return self.value.__rpow__(other)

	def __rrshift__(self, other):
		return self.value.__rrshift(other)

	def __rsub__(self, other):
		return self.value.__rsub__(other)

	def __rtruediv__(self, other):
		return self.value.__rtruediv__(other)

	def __rxor__(self, other):
		return self.value.__rxor__(other)

	# end

	#
	# commented out
	#

	"""
	# def __eq__(self, other):  # overridden
	# 	return self.value.__eq__(other)

	def __getitem__(self, item):
		return self.value.__getitem__(item)

	def __aenter__(self):
		return self.value.__aenter__()

	def __aexit__(self, exc_type, exc_val, exc_tb):
		return self.value.__aexit__(exc_type, exc_val, exc_tb)

	def __aiter__(self):
		return self.value.__aiter__()

	def __anext__(self):
		return self.value.__anext__()

	def __await__(self):
		return self.value.__await__()

	def __bool__(self):
		return self.value.__bool__()

	def __bytes__(self):
		return self.value.__bytes__()

	def __call__(self, *args, **kwargs):
		return self.value.__call__(*args, **kwargs)

	# def __class_getitem__(cls, item):  # error
	# 	return cls.value.__class_getitem__(item)

	def __cmp__(self, other):
		return self.value.__cmp__(other)

	def __coerce__(self, other):
		return self.value.__coerece__(other)

	def __complex__(self):
		return self.value.__complex__()

	def __contains__(self, item):
		return self.value.__contains__(item)

	def __copy__(self):
		return self.value.__copy__()

	# noinspection PyDefaultArgument
	def __deepcopy__(self, memodict={}):
		return self.value.__deepcopy__(memodict)

	# def __del__(self):  # causes error
	# 	return self.value.__del__()

	def __delattr__(self, item):
		return self.value.__delattr__(item)

	def __delete__(self, instance):
		return self.value.__delete__(instance)

	def __delitem__(self, key):
		return self.value.__delitem__(key)

	def __delslice__(self, i, j):
		return self.value.__delslice__(i, j)

	# def __dir__(self) -> Iterable[str]:  # throws an error
	# 	pass

	# def __divmod__(self, other):  # overridden
	# 	return self.value.__divmod__(other)

	def __enter__(self):
		return self.value.__enter__()

	def __exit__(self, exc_type, exc_val, exc_tb):
		return self.value.__exit__(exc_type, exc_val, exc_tb)

	def __float__(self):
		return self.value.__float__()

	def __format__(self, format_spec):
		return self.value.__format(format_spec)

	def __fspath__(self):
		return self.value.__fspath__()

	# def __ge__(self, other):  # overridden
	# 	return self.value.__ge__(other)

	def __get__(self, instance, owner):
		return self.value.__get__(instance, owner)

	def __getattr__(self, item):
		return self.value.__getattr__(item)

	# def __getattribute__(self, item):  # causes error
	# 	return self.value.__getattribute__(item)

	def __getinitargs__(self):
		return self.value.__getinitargs__()

	def __getnewargs__(self):
		return self.value.__getnewargs()

	def __getstate__(self):
		return self.value.__getstate__()

	# def __gt__(self, other):  # overridden
	# 	return self.value.__gt__(other)

	def __hash__(self):
		return self.value.__hash__()

	def __hex__(self):
		return self.value.__hex__()

	def __index__(self):
		return self.value.__index__()

	# def __init_subclass__(cls, **kwargs):  # causes error
	# 	return cls.value.__init_subclass__(**kwargs)

	def __instancecheck__(self, instance):
		return self.value.__instancecheck__(instance)

	def __int__(self):
		return self.value.__int__()

	def __iter__(self):
		return self.value.__iter__()

	# def __le__(self, other):  # overridden
	# 	return self.value.__le__(other)

	def __len__(self):
		return self.value.__len__()

	def __long__(self):
		return self.value.__long__()

	# def __lt__(self, other):  # overridden
	# 	return self.value.__lt__(other)

	def __missing__(self, key):
		return self.value.__missing__(key)

	def __mro_entries__(self, bases):
		return self.value.__mro_entries__(bases)

	# def __ne__(self, other):  # overridden
	# 	return self.value.__ne__(other)

	# def __new__(cls, *args, **kwargs):  # causes errors
	# 	return cls.value.__new__(*args, **kwargs)

	def __next__(self):
		return self.value.__next__()

	def __oct__(self):
		return self.value.__oct__()

	def __pos__(self):
		return self.value.__pos__()

	# noinspection PyMethodParameters,PyProtectedMember
	# @classmethod
	# def __prepare__(mcs, name, bases):
	# 	return mcs.value.__prepare__(name, bases)

	def __reduce__(self):
		return self.value.__reduce__()

	def __reduce_ex__(self, protocol):
		return self.value.__reduce_ex__(protocol)

	def __repr__(self):
		return self.value.__repr__()

	def __reversed__(self):
		return self.value.__reversed__()

	def __round__(self, n=None):
		return self.value.__round__(n)

	# def __rshift__(self, other):  # overridden
	# 	return self.value.__rshift__(other)

	def __set__(self, instance, value):
		return self.value.__set__(instance, value)

	def __set_name__(self, owner, name):
		return self.value.__set_name__(owner, name)

	# def __setattr__(self, key, value):  # causes error
	# 	return self.value.__setattr__(key, value)

	def __setitem__(self, key, value):
		return self.value.__setitem__(key, value)

	def __setslice__(self, i, j, sequence):
		return self.value.__setslice__(i, j, sequence)

	def __setstate__(self, state):
		return self.value.__setstate__(self, state)

	def __sizeof__(self):
		return self.value.__sizeof__()

	def __str__(self):
		return self.value.__str__()

	def __subclasscheck__(self, subclass):
		return self.value.__subclasscheck__(subclass)

	def __trunc__(self):
		return self.value.__trunc__()

	def __unicode__(self):
		return self.value.__unicode__()
	"""


if __name__ == "__main__":
	class A(AutoValue):
		@property
		def value(self):
			return self._value

		@value.setter
		def value(self, x):
			self._value = x

		def __init__(self):
			self.value = 0

	a = A()
	a += 8

	print(a.value)
	print(a == 8)
