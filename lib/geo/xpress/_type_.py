

from . import _ops_ as ops


class AutoOperators:
	# override these
	def __eq__(self, other):
		pass

	def __lt__(self, other):
		pass

	def __add__(self, other):
		pass

	def __sub__(self, other):
		pass

	def __mul__(self, other):
		pass

	def __truediv__(self, other):
		pass

	def __floordiv__(self, other):
		pass

	def __mod__(self, other):
		pass

	def __pow__(self, power, modulo=None):
		pass

	def __and__(self, other):
		pass

	def __or__(self, other):
		pass

	def __xor__(self, other):
		pass

	def __lshift__(self, other):
		pass

	def __rshift__(self, other):
		pass

	# comparisons
	def __gt__(self, other):
		return other.__lt__(self)

	def __ne__(self, other):
		return not self.__eq__(other)

	def __ge__(self, other):
		return not self.__lt__(other)

	def __le__(self, other):
		return not self.__gt__(other)

	# self assignment
	def __iadd__(self, other):
		return self.__add__(other)

	def __isub__(self, other):
		return self.__sub__(other)

	def __imul__(self, other):
		return self.__mul__(other)

	def __itruediv__(self, other):
		return self.__truediv__(other)

	def __ifloordiv__(self, other):
		return self.__floordiv__(other)

	def __imod__(self, other):
		return self.__mod__(other)

	def __ipow__(self, power, modulo=None):
		return self.__pow__(power, modulo=modulo)

	def __iand__(self, other):
		return self.__and__(other)

	def __ior__(self, other):
		return self.__or__(other)

	def __ixor__(self, other):
		return self.__xor__(other)

	def __ilshift__(self, other):
		return self.__lshift__(other)

	def __irshift__(self, other):
		return self.__rshift__(other)


class Expression(AutoOperators):
	class Identity:
		# todo use this to create identities for simplification
		# will need separate systems for formula identities and value identities
		def __init__(self, function, args, kwargs):
			self.function = function
			self.positionals = len(args)
			self.keywords = set(kwargs)
			return

		def __hash__(self):
			return hash(str(self.function.__name__) + str(self.positionals) + str(self.keywords))

	@staticmethod
	def dummy(*args, **kwargs):
		pass

	@staticmethod
	def no_operation(*args, **kwargs):
		del kwargs
		if len(args) == 1:
			return args[0]
		raise ValueError("! wrong number of args for function 'no_operation'")

	def eval(self):
		f = self.no_operation if self.function is None else self.function
		args = (v.eval() if isinstance(v, Expression) else v for v in self.args)
		kwargs = {k: v.eval() if isinstance(v, Expression) else v for k, v in self.kwargs.items()}
		return f(*args, **kwargs)

	def __init__(self, function, *args, **kwargs):
		self.function = function
		self.args = args
		self.kwargs = kwargs
		return

	def __repr__(self):
		args = ""
		for arg in self.args:
			args += f", {repr(arg)}"
		kwargs = ""
		for k, v in self.kwargs.items():
			kwargs += f", {k}={repr(v)}"
		return f"{self.__class__.__name__}({repr(self.function.__name__ if self.function else None)}{args}{kwargs})"

	def __eq__(self, other):
		return Expression(ops.eq, self, other)

	def __lt__(self, other):
		return Expression(ops.lt, self, other)

	def __add__(self, other):
		return Expression(ops.add, self, other)

	def __sub__(self, other):
		return Expression(ops.sub, self, other)

	def __mul__(self, other):
		return Expression(ops.mul, self, other)

	def __truediv__(self, other):
		return Expression(ops.truediv, self, other)

	def __floordiv__(self, other):
		return Expression(ops.floordiv, self, other)

	def __mod__(self, other):
		return Expression(ops.mod, self, other)

	def __pow__(self, power, modulo=None):
		return Expression(ops.pow, self, power, modulo=modulo)

	def __and__(self, other):
		return Expression(ops.xnd, self, other)

	def __or__(self, other):
		return Expression(ops.xr, self, other)

	def __xor__(self, other):
		return Expression(ops.xor, self, other)

	def __invert__(self):
		return Expression(ops.inv, self)

	def __lshift__(self, other):
		return Expression(ops.lshift, self, other)

	def __rshift__(self, other):
		return Expression(ops.rshift, self, other)

	# right side fall backs
	def __radd__(self, other):
		return Expression(ops.add, other, self)

	def __rsub__(self, other):
		return Expression(ops.sub, other, self)

	def __rmul__(self, other):
		return Expression(ops.mul, other, self)

	def __rtruediv__(self, other):
		return Expression(ops.truediv, other, self)

	def __rfloordiv__(self, other):
		return Expression(ops.floordiv, other, self)

	def __rmod__(self, other):
		return Expression(ops.mod, other, self)

	def __rpow__(self, power, modulo=None):
		return Expression(ops.pow, power, self, modulo=modulo)

	def __rand__(self, other):
		return Expression(ops.xnd, other, self)

	def __ror__(self, other):
		return Expression(ops.xr, other, self)

	def __rxor__(self, other):
		return Expression(ops.xor, other, self)

	def __rlshift__(self, other):
		return Expression(ops.lshift, other, self)

	def __rrshift__(self, other):
		return Expression(ops.rshift, other, self)
