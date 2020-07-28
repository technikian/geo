from ..vector import Vector as Vector


class Tensor(Vector):
	# technical name for a matrix of >2 dimensions is tensor

	# recursively indexes the dimensions
	# this works in big endian
	class Nested:  # nested tensor
		class Iter:
			def __init__(self, parent_nested_tensor):
				self.parent = parent_nested_tensor
				self.index = 0
				self.limit = len(parent_nested_tensor)
				return

			def __iter__(self):
				return self

			def __next__(self):
				if self.index == self.limit:
					raise StopIteration
				r = self.parent[self.index]
				self.index += 1
				return r

		class ReverseIter:
			def __init__(self, parent_nested_tensor):
				self.parent = parent_nested_tensor
				self.index = len(parent_nested_tensor) - 1
				self.limit = -1
				return

			def __iter__(self):
				return self

			def __next__(self):
				if self.index == self.limit:
					raise StopIteration
				r = self.parent[self.index]
				self.index -= 1
				return r

		def __init__(self, parent_tensor, depth, index):
			self.parent = parent_tensor
			self.depth = depth
			self.index = index
			self.step = self.parent.steps[~depth]
			return

		def __len__(self):
			return self.parent.order[~self.depth]

		def __iter__(self):
			return self.Iter(self)

		def __reversed__(self):
			return self.ReverseIter(self)

		def __getitem__(self, item):
			try:
				depth = self.depth + 1
				index = self.index + item * self.step
				if depth == len(self.parent.order):
					r = self.parent.values[index]
					return r
				return Tensor.Nested(self.parent, depth, index)
			except IndexError:
				raise IndexError("! tensor index out of bounds.")

		def __setitem__(self, key, value):
			try:
				depth = self.depth + 1
				index = self.index + key * self.step
				if depth == len(self.parent.order):
					self.parent.values[index] = value
					return
				return Tensor.Nested(self.parent, depth, index)
			except IndexError:
				raise IndexError("! tensor index out of bounds.")

	class Dimension:
		"""represents an array of a single tensor dimension"""

		@property
		def index(self):
			return self.indexes.index(None)

		@classmethod
		def from_indexes(cls, parent_tensor, indexes):
			"""find the items by the dimension indexes"""
			index = indexes.index(None)
			values = tuple(
				parent_tensor.__getitem__((*indexes[:index], i, *indexes[index + 1:]))
				for i in range(parent_tensor.order[index]))
			return cls(parent_tensor, indexes, values)

		def __init__(self, parent_tensor, indexes, values):
			self.parent = parent_tensor
			self.indexes = indexes
			self.values = values

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

	def dimension(self, *indexes):
		"""get an individual dimension as an array
		tensor must have order > a * b"""
		return self.Dimension.from_indexes(self, indexes)

	# little-endian tensor order

	@property
	def order(self):
		return self._m_Tensor_order

	@order.setter
	def order(self, value):
		self._m_Tensor_order = tuple(value)  # tuple is immutable, therefore this doesn't copy
		self.steps = tuple((1, *value[:-1]))

	def __init__(self, order, values=(), cont_t=list):
		"""order (tuple of dimension lengths), (initialization) values, default (initialization value)
		"""
		super().__init__(values, cont_t)
		self.order = order

	def __repr__(self):
		return f"Tensor({repr(self.order)}, {repr(self.values)})"

	def __len__(self):
		try:
			return self.order[-1]
		except IndexError:
			return 0

	def __iter__(self):
		return self.Nested(self, 0, 0).__iter__()

	def __reversed__(self):
		return self.Nested(self, 0, 0).__reversed__()

	def __getitem__(self, item):
		if not isinstance(item, tuple):
			return self.Nested(self, 0, 0)[item]
		i = 0
		for step, k in zip(self.steps, item):
			i += k * step
		return self.values[i]

	def __setitem__(self, key, value):
		i = 0
		for step, k in zip(self.steps, key):
			i += k * step
		self.values[i] = value

	def __lt__(self, other):
		return NotImplemented

	def __eq__(self, other):
		if self.order != other.order:
			return False
		return Vector.__eq__(self, other)

	def is_eractical(self):
		"""all dimensions of equal length"""
		for v in self.order:
			if v != len(self):
				return False
		return True


class TensorMap:
	pass
