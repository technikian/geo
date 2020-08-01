from geo import Matrix
from random import randint


def mat_print(mat):
	r = ""
	for major in mat:
		for minor in major:
			r += f"{minor} "
		r += "\n"
	print(r[:])


def mat_print_row_maj(mat):
	r = ""
	for major in range(mat.order[1]):
		for minor in range(mat.order[0]):
			r += f"{mat[major, minor]} "
		r += "\n"
	print(r[:])


if __name__ == "__main__":
	old_m = ((1, 2, 3), (4, 5, 6), (7, 8, 9))
	m = Matrix((1, 2, 3, 4, 5, 6, 7, 8, 10), 3, 3)
	# row major
	mat_print_row_maj(m.transpose())
	mat_print_row_maj(m.transpose().minor(0, 1))
	# col major
	mat_print(m)
	mat_print(m.minor(1, 0))

	print(m.determinant())
	n = Matrix((randint(-100, 100) for i in range(9)), 3, 3)
	print(n.determinant())
	print(n.transpose().determinant())

	mat_print(m * 2)
	mat_print(m.adjugate())
	mat_print(~m)

	o = Matrix((1, 2, 3, 4, 5, 6), 3, 2)
	mat_print(o.cross(m))
