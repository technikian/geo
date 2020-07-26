
# includes
from copy import deepcopy as _m_deepcopy
from ..tensor import Tensor as _m_Tensor


#
# comparisons
#

def is_square(matrix):
	try:
		if len(matrix) == len(matrix[0]):
			return len(matrix)
	except IndexError:
		pass
	return -1


def rows(matrix):
	return len(matrix)


def cols(matrix):
	try:
		return len(matrix[0])
	except IndexError:
		return 0


def eq(a, b):
	for ax, bx in zip(a, b):
		for ay, by in zip(ax, bx):
			if ay != by:
				return False
	return True


#
# operations
#

def iadd(a, b):
	m = rows(a)
	n = cols(a)
	if rows(b) != m or cols(b) != n:
		raise ValueError("! matrices must be of same size")
	for i, bx in zip(range(m), b):
		for j, by in zip(range(n), bx):
			a[i][j] += by
	return


def isub(a, b):
	m = rows(a)
	n = cols(a)
	if rows(b) != m or cols(b) != n:
		raise ValueError("! matrices must be of same size")
	for i, bx in zip(range(m), b):
		for j, by in zip(range(n), bx):
			a[i][j] -= by
	return


def add(a, b):
	r = _m_deepcopy(a)
	iadd(r, b)
	return r


def sub(a, b):
	r = _m_deepcopy(a)
	isub(r, b)
	return r


def mul(a, b):
	# scalar multiplication
	if not hasattr(b, "__getitem__"):
		result = _m_Tensor((rows(a), cols(a)))
		for i in range(len(a)):
			for j in range(len(a[i])):
				result[i][j] = a[i][j] * b

	# matrix multiplication
	else:
		result = _m_Tensor((rows(a), cols(b)))
		size = cols(a)
		if size != rows(b):
			raise ValueError("! matrix b must have same number of columns as matrix a has rows")
		# traverse rows
		result_row = -1
		for a_row in a:
			result_row += 1
			# traverse columns
			result_col = -1
			for b_col_i in range(cols(b)):
				result_col += 1
				# do multiplication
				temp = type(a[0][0])(0)
				b_row_i = -1
				for a_col in a_row:
					b_row_i += 1
					temp += a_col * b[b_row_i][b_col_i]
				# save result
				result[result_row][result_col] = temp

	return result


# def imul(a, b):
# 	r =


#
# functions
#

# note - rows and columns may be swapped without affecting determinant
def minor(matrix, row, col):
	_rows = rows(matrix)
	_cols = cols(matrix)
	r = _m_Tensor((_rows - 1, _cols - 1))
	tgt_i = 0
	for i, x in zip(range(_rows), matrix):
		if i == row:
			continue
		tgt_j = 0
		for j, y in zip(range(_cols), x):
			if j == col:
				continue
			r[tgt_i][tgt_j] = y
			tgt_j += 1
		tgt_i += 1
	return r


def minors(matrix, row):
	return (minor(matrix, row, i) for i in range(rows(matrix)))
	# minors = []
	# for i in range(len(matrix[row])):
	# 	minors.append(minor(matrix, row, i))
	# return minors


def determinant_2(matrix):
	try:
		return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
	except IndexError:
		raise IndexError("! matrix needs to be of dimensions 2*2")


def determinant_3(matrix):
	try:
		# cross-right
		r = matrix[0][0] * matrix[1][1] * matrix[2][2]
		r += matrix[0][1] * matrix[1][2] * matrix[2][0]
		r += matrix[0][2] * matrix[1][0] * matrix[2][1]
		# cross-left
		r -= matrix[0][0] * matrix[1][2] * matrix[2][1]
		r -= matrix[0][1] * matrix[1][0] * matrix[2][2]
		r -= matrix[0][2] * matrix[1][1] * matrix[2][0]
		return r
	except IndexError:
		raise IndexError("! matrix needs to be of dimensions 3*3")


def determinant(matrix):
	size = is_square(matrix)
	if size > 3:
		row_of_minors = minors(matrix, 0)
		r = type(matrix[0][0])(0)  # init the result to 0, same type as 0, 0 in source matrix
		column = -1
		negate = True  # is negative
		for m in row_of_minors:
			column += 1     # column index
			negate ^= True  # toggle negative
			if negate:
				r -= matrix[0][column] * determinant(m)
			else:
				r += matrix[0][column] * determinant(m)
		return r
	if size == 3:
		return determinant_3(matrix)
	if size == 2:
		return determinant_2(matrix)
	if size == 1:
		return matrix[0][0]
	if size == 0:
		return 0
	raise ValueError("! matrix needs to be square to find the determinant")


def transpose(matrix):
	# construct a new matrix with rows and cols inverted
	r = _m_Tensor((cols(matrix), rows(matrix)))
	# traverse rows
	target_col = -1
	for source_row in matrix:
		target_col += 1
		# traverse columns
		target_row = -1
		for source_col in source_row:
			target_row += 1
			r[target_row][target_col] = source_col
	return r


def cofactor(matrix):
	m = rows(matrix)
	n = cols(matrix)
	r = _m_Tensor((m, n))
	# traverse rows
	for row in range(m):
		for col in range(n):
			if (row + col) % 2:
				r[row][col] = -determinant(minor(matrix, row, col))
			else:
				r[row][col] = determinant(minor(matrix, row, col))
	return r


def adjugate(matrix):
	r = cofactor(matrix)
	r = transpose(r)
	return r


def inverse(matrix):
	if not is_square(matrix):
		raise ValueError("! non-square matrix cannot be inverted")
	det = determinant(matrix)
	if det == 0:
		raise ZeroDivisionError("! matrix has no inverse as determinant is zero")
	adj = adjugate(matrix)
	r = mul(adj, 1 / det)
	return r
