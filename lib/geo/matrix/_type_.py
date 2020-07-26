from ..tensor import Tensor as Tensor
from ._ops_ import mul as _mul, inverse as _inverse


class Matrix(Tensor):
	@property
	def m_length(self):
		"""number of rows"""
		return self.order[0]

	@property
	def n_length(self):
		"""number of columns"""
		return self.order[1]

	@classmethod
	def from_tensor(cls, tensor):
		return cls(tensor.order[0], tensor.order[1], tensor.scope)

	def __init__(self, m, n, values=(), cont_t=list):
		super().__init__((m, n), values, cont_t)

	def __repr__(self):
		# todo repr can't handle large strings
		# print(self.values.__len__())
		# print(tuple(self.values))  # bad
		values = self.values
		values = repr(values[:128]) + ("..." if len(values) > 127 else "")
		# values = ""
		return f"Matrix({repr(self.order[0])}, {repr(self.order[1])}, {values})"

	def __invert__(self):
		return _inverse(self)

	def __mul__(self, other):
		return _mul(self, other)

	def __imul__(self, other):
		r = _mul(self, other)
		self.wrappers = r.values
		self.order = r.order
		self.steps = r.steps
		return self
