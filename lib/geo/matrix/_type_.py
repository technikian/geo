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

	# @classmethod
	# def from_tensor(cls, tensor):
	# 	return cls(tensor.order[0], tensor.order[1], tensor.scope)

	def __init__(self, m, n, values=(), cont_t=list):
		super().__init__((m, n), values, cont_t)

	def __repr__(self):
		# todo repr can't handle large strings
		# print(self.values.__len__())
		# print(tuple(self.values))  # bad
		values = self.values
		values = repr(values[:128]) + ("..." if len(values) > 127 else "")
		# values = ""
		return f"Matrix({repr(self.order[1:-1])}, {repr(values)})"

	# def __invert__(self):
	# 	return _inverse(self)

	# def __mul__(self, other):
	# 	return _mul(self, other)

	# def __imul__(self, other):
	# 	r = _mul(self, other)
	# 	self.wrappers = r.values
	# 	self.order = r.order
	# 	self.steps = r.steps
	# 	return self

	# scalar product
	def scale(self, other):
		return Matrix(self.m_length, self.n_length, (other * v for v in self.values), type(self.values))

	# dot product
	def dot(self, other):
		# TODO
		pass

	# cross product
	def cross(self, other):
		pass

	#
	# transformations
	#

	def minors(self):
		pass

	def minor(self, m, n):
		pass

	def _determinant_3(self):
		# independent of row/col major
		# cross-right (row, col)
		r = self[0, 0] * self[1, 1] * self[2, 2]
		r += self[0, 1] * self[1, 2] * self[2, 0]
		r += self[0, 2] * self[1, 0] * self[2, 1]
		# cross-left (row, col)
		r -= self[0, 0] * self[1, 2] * self[2, 1]
		r -= self[0, 1] * self[1, 0] * self[2, 2]
		r -= self[0, 2] * self[1, 1] * self[2, 0]
		return r

	def _determinant_2(self):
		# independent of row/col major
		return self[0, 0] * self[1, 1] - self[0, 1] * self[1, 0]

	def determinant(self):
		size = min(self.n_length, self.m_length)  # this may chop matrix to make it square
		if size > 3:
			row_of_minors = minors(matrix, 0)
			r = type(matrix[0][0])(0)  # init the result to 0, same type as 0, 0 in source matrix
			column = -1
			negate = True  # is negative
			for minor in row_of_minors:
				column += 1  # column index
				negate ^= True  # toggle negative
				if negate:
					r -= matrix[0][column] * determinant(minor)
				else:
					r += matrix[0][column] * determinant(minor)
			return r
		if size == 3:
			return self._determinant_3()
		if size == 2:
			return self._determinant_2()
		if size == 1:
			return self.values[0]
		if size == 0:
			return 0
		raise ValueError("! matrix needs to be square to find the determinant")

	def transpose(self):
		values = (v for i in range(self.order[0]) for v in self.dimension(i, None))
		return Matrix(self.n_length, self.m_length, values, cont_t=type(self.values))

	def cofactor(self):
		# TODO
		return self

	def adjugate(self):
		return self.cofactor().transpose()

	def __invert__(self):  # inverse (only works on square matrix)
		if self.m_length != self.n_length:
			raise ValueError("! non-square matrix cannot be inverted")
		return self.adjugate() * (1 / self.determinant())


class MatrixMap:
	pass
