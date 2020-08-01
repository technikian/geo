from .._core_.enum import Enum, Selector
from ..tensor import Tensor as Tensor


class Matrix(Tensor):
	# todo revise what is row/col major, swap below args (column, row):
	# especially check non-commutative (cross product, cofactor, adjugate, inverse)
	DIMENSION_MAJOR = Enum(column=1, row=0)  # xor 0 makes no change, xor 1 makes flip
	DEFAULT_DIMENSION_MAJOR = 0
	# order[0] is col, order[1] is row for row major
	DEFAULT_M_INDEX = 1
	DEFAULT_N_INDEX = 0

	@property
	def m(self):
		"""number of rows"""
		return self.order[self.DEFAULT_M_INDEX ^ self.dimension_major.value]

	@property
	def n(self):
		"""number of columns"""
		return self.order[self.DEFAULT_N_INDEX ^ self.dimension_major.value]

	@property
	def x(self):
		"""minor dimension size"""
		return self.order[0]

	@property
	def y(self):
		"""major dimension size"""
		return self.order[1]

	@classmethod
	def from_args(cls, iterable=(), order=(-1, 1), cont_t=list):
		return cls(iterable, order[0], order[1], cont_t)

	def __init__(self, values=(), x=-1, y=1, cont_t=list):
		super().__init__(values, (x, y), cont_t)
		self.dimension_major = Selector(self.DIMENSION_MAJOR, self.DEFAULT_DIMENSION_MAJOR)

	def __repr__(self):
		values = self.values
		values = repr(values[:self.MAX_VALUES_FOR_REPR]) + (" ..." if len(values) >= self.MAX_VALUES_FOR_REPR else "")
		return f"Matrix({values}, {self.order[0]}, {self.order[1]})"

	# scalar product
	def scale(self, other):
		return Matrix((other * v for v in self.values), self.order[0], self.order[1], type(self.values))

	# dot product
	def dot(self, other):
		# TODO
		pass

	# cross product
	def cross(self, other):
		# organize
		# row major
		a = self
		b = other
		minor_len = a.x  # default: columns of a = rows of b
		major_len = b.y  # this is row if row major
		if minor_len != major_len:
			raise ValueError("! matrix b must have same number of rows as matrix a has cols")
		# do the calculations
		# since a has same rows as b has columns:
		#  multiply each a_row item with each b_col item
		#   sum all items where a_row_index = b_col_index
		rows_a = (self.dimension(None, i) for i in range(a.y))  # generator
		cols_b = tuple(other.dimension(i, None) for i in range(b.x))  # used multiple times, so make as tuple
		# sum(i * j for i, j in zip(rows_a[0], cols_b[0]))  calculates a single value
		# in case the list comprehension is incomprehensible
		# values = []
		# for row in rows_a:
		# 	for col in cols_b:
		# 		values.append(sum(i * j for i, j in zip(row, col)))
		values = tuple((sum(i * j for i, j in zip(row, col)) for row in rows_a for col in cols_b))
		return type(self)(values, other.x, self.y, type(self.values))

	#
	# transformations
	#

	def minor(self, x, y):
		"""x: minor index, y: major index"""
		values = (minor for j, major in enumerate(self) for i, minor in enumerate(major) if i != x and j != y)
		return Matrix(values, self.order[0] - 1, self.order[1] - 1, type(self.values))

	def determinant_3(self):
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

	def determinant_2(self):
		# independent of row/col major
		return self[0, 0] * self[1, 1] - self[0, 1] * self[1, 0]

	def determinant(self):
		# independent of row/col major
		# variable names assume little endian, row major
		size = min(self.order[0], self.order[1])  # this may chop matrix to make it square
		if size > 3:
			# init the result to 0, same type as 0, 0 in source matrix
			r = self.values[0]
			r -= r
			row_of_minors = tuple(self.minor(x, 0) for x in range(size))
			negate = True  # is negative
			for x, minor in zip(self[0], row_of_minors):
				negate ^= True  # toggle negative
				if negate:
					r -= x * minor.determinant()
				else:
					r += x * minor.determinant()
			return r
		if size == 3:
			return self.determinant_3()
		if size == 2:
			return self.determinant_2()
		if size == 1:
			return self.values[0]
		if size == 0:
			return 0
		raise ValueError("! matrix needs to be square to find the determinant")

	def transpose(self):
		"""switch rows with columns"""
		# independent of row/col major
		values = (v for i in range(self.order[0]) for v in self.dimension(i, None))
		return Matrix(values, self.order[0], self.order[1], type(self.values))

	def cofactor(self):
		values = (
			-self.minor(i, j).determinant() if (i + j) % 2 else self.minor(i, j).determinant()
			for j, major in enumerate(self) for i, minor in enumerate(major)
		)
		return Matrix(values, self.order[0], self.order[1], type(self.values))

	def adjugate(self):  # aka adjoint
		return self.cofactor().transpose()

	def __invert__(self):  # inverse (only works on square matrix)
		if self.order[0] != self.order[1]:
			raise ValueError("! non-square matrix has no inverse")
		det = self.determinant()
		if det == 0:
			raise ZeroDivisionError("! determinant = 0, matrix has no inverse")
		return self.adjugate() / det


class MatrixMap:
	pass
