from .._core_.base import Comparable


# vector may be used as key-path
# noinspection PyArgumentList
class Vector(Comparable):
	MAX_VALUES_FOR_REPR = 128

	@classmethod
	def from_args(cls, iterable=(), order=(-1,), cont_t=list):
		return cls(iterable, cont_t)

	def __init__(self, iterable=(), cont_t=list):
		self.values = iterable if isinstance(iterable, cont_t) else cont_t(iterable)

	def __repr__(self):
		# repr can't handle large strings for some reason
		values = self.values
		values = repr(values[:self.MAX_VALUES_FOR_REPR]) + (" ..." if len(values) >= self.MAX_VALUES_FOR_REPR else "")
		return f"Vector({values})"

	def __hash__(self):
		return hash((self.order, self.values))

	@property
	def order(self):
		return len(self.values),

	def __len__(self):
		return len(self.values)

	def __iter__(self):
		return iter(self.values)

	def __reversed__(self):
		return reversed(self.values)

	def __getitem__(self, item):
		return self.values[item]

	def __setitem__(self, key, value):
		self.values[key] = value

	#
	# define compare operators
	#

	def __lt__(self, other):
		"""reverse lexicographical compare: maintains little-endian standardization
		(aka co-lexicographical compare)"""
		if len(self) < len(other):
			return True
		for a, b in zip(reversed(self.values), reversed(other)):
			if a < b:
				return True
		return False

	def __eq__(self, other):
		if len(self) != len(other):
			return False
		for a, b in zip(self.values, other):
			if a != b:
				return False
		return True

	#
	# define translation operators
	#

	# for testing.  slower, but easier to fix mistakes
	# for release versions, bake these operations in code to be faster (but not dynamic)
	def _op_(self, other, function):
		values = self.values
		self_t = type(self)
		cont_t = type(values)
		if hasattr(other, "__iter__"):
			return self_t.from_args((function(a, b) for a, b in zip(values, other)), self.order, cont_t)
		return self_t.from_args((function(a, other) for a in values), self.order, cont_t)

	def _iop_(self, other, function):
		"""self-op"""
		if hasattr(other, "__iter__"):
			for i, b in zip(range(len(self.values)), other):
				# self[i] += b
				self[i] = function(self[i], b)  # index, other
		else:
			for i, b in self.values:
				# self[i] += other
				self[i] = function(self[i], other)  # index, other
		return self

	def __neg__(self):
		values = self.values
		return type(self).from_args((-a for a in values), self.order, type(values))

	def __add__(self, other):
		return self._op_(other, lambda a, b: a + b)

	def __iadd__(self, other):
		return self._iop_(other, lambda a, b: a + b)

	def __radd__(self, other):
		return self + other

	def __sub__(self, other):
		return self._op_(other, lambda a, b: a - b)

	def __isub__(self, other):
		return self._iop_(other, lambda a, b: a - b)

	def __rsub__(self, other):
		return (-self) + other

	#
	# multiplication
	#

	# default method is element-wise

	def __mul__(self, other):
		return self._op_(other, lambda a, b: a * b)

	def __imul__(self, other):
		return self._iop_(other, lambda a, b: a * b)

	def __rmul__(self, other):
		return self * other

	def __truediv__(self, other):
		return self._op_(other, lambda a, b: a / b)

	def __itruediv__(self, other):
		return self._iop_(other, lambda a, b: a / b)

	def __rtruediv__(self, other):
		# doesn't matter that this wont work for non-iterable other
		r = type(self).from_args(other, self.order)
		r /= self
		return r

	def __floordiv__(self, other):
		return self._op_(other, lambda a, b: a // b)

	def __ifloordiv__(self, other):
		return self._iop_(other, lambda a, b: a // b)

	def __rfloordiv__(self, other):
		# doesn't matter that this wont work for non-iterable other
		r = type(self).from_args(other, self.order)
		r //= self
		return r

	# dot product
	def dot(self, other):
		values = (a * b for a, b in zip(self.values, other))
		r = next(values)
		for value in values:
			r += value
		return r

	# cross product
	def cross(self, other):
		# TODO
		pass

	# end


# Dict-like vector
# noinspection SpellCheckingInspection
class VectorMap:
	def __init__(self, mappings):
		self.mappings = mappings if isinstance(mappings, dict) else dict(mappings)

	def __repr__(self):
		return f"VectorMap({repr(self.mappings)})"

	def __hash__(self):
		return hash((self.order, self.mappings.items()))

	@property
	def order(self):
		return len(self.mappings),

	def __len__(self):
		return len(self.mappings)

	def __iter__(self):
		return iter(self.mappings)

	def __reversed__(self):
		return reversed(self.mappings)

	def __getitem__(self, item):
		return self.mappings[item]

	def __setitem__(self, key, value):
		self.mappings[key] = value

	#
	# define compare operators
	#

	# no < operator as of now todo look into

	def __eq__(self, other):
		if len(self) != len(other):
			return False
		for ak, av, bk in zip(*self.mappings.items(), other):
			if ak != bk:
				return False
			if av != other[bk]:
				return False
		return True

	#
	# define translation operators
	#

	def __neg__(self):
		return Vector(type(self.mappings)({k: -v for k, v in self.mappings.items()}))

	def __add__(self, other):  # note: other may not be of the same type
		if len(self) != len(other):
			raise ValueError("! Vectors of different length")
		return Vector(type(self.mappings)({k: v + other[k] for k, v in self.mappings.items()}))

	def __iadd__(self, other):
		if len(self) != len(other):
			raise ValueError("! Vectors of different length")
		for k in self.mappings:
			self[k] += other[k]
		return self

	def __radd__(self, other):
		return self + other

	def __sub__(self, other):
		if len(self) != len(other):
			raise ValueError("! Vectors of different length")
		return Vector(type(self.mappings)({k: v - other[k] for k, v in self.mappings.items()}))

	def __isub__(self, other):
		if len(self) != len(other):
			raise ValueError("! Vectors of different length")
		for k in self.mappings:
			self[k] -= other[k]
		return self

	def __rsub__(self, other):
		return (-self) + other

	#
	# multiplication
	#

	# default method is element-wise

	def __mul__(self, other):
		if len(self) != len(other):
			raise ValueError("! Vectors of different length")
		return Vector(type(self.mappings)({k: v * other[k] for k, v in self.mappings.items()}))

	def __imul__(self, other):
		if len(self) != len(other):
			raise ValueError("! Vectors of different length")
		for k in self.mappings:
			self[k] *= other[k]
		return self

	def __rmul__(self, other):
		return self * other

	def __truediv__(self, other):
		if len(self) != len(other):
			raise ValueError("! Vectors of different length")
		return Vector(type(self.mappings)({k: v / other[k] for k, v in self.mappings.items()}))

	def __itruediv__(self, other):
		if len(self) != len(other):
			raise ValueError("! Vectors of different length")
		for k in self.mappings:
			self[k] /= other[k]
		return self

	def __rtruediv__(self, other):
		r = Vector(other)
		r /= self
		return r

	def __floordiv__(self, other):
		if len(self) != len(other):
			raise ValueError("! Vectors of different length")
		return Vector(type(self.mappings)({k: v // other[k] for k, v in self.mappings.items()}))

	def __ifloordiv__(self, other):
		if len(self) != len(other):
			raise ValueError("! Vectors of different length")
		for k in self.mappings:
			self[k] //= other[k]
		return self

	def __rfloordiv__(self, other):
		r = Vector(other)
		r //= self
		return r

	# dot product
	def dot(self, other):
		# TODO
		pass

	# cross product
	def cross(self, other):
		pass

	# end
