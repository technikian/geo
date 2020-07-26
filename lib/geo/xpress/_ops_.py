

def cmp(operator, args):
	itx = iter(args)
	r = None
	try:
		current = next(itx)
		while True:
			last = current
			current = next(itx)
			r = operator(last, current)
			if not r:
				return False
	except StopIteration:
		return r


# noinspection PyShadowingBuiltins
def eval(operator, args):
	itx = iter(args)
	r = None
	try:
		r = next(itx)
		while True:
			r = operator(r, next(itx))
	except StopIteration:
		return r


def eq(*args):
	def f(a, b):
		return a == b
	return cmp(f, args)


def lt(*args):
	def f(a, b):
		return a < b
	return cmp(f, args)


def gt(*args):
	def f(a, b):
		return a > b
	return cmp(f, args)


def ne(*args):
	def f(a, b):
		return a != b
	return cmp(f, args)


def ge(*args):
	def f(a, b):
		return a >= b
	return cmp(f, args)


def le(*args):
	def f(a, b):
		return a <= b
	return cmp(f, args)


#
#
#

def add(*args):
	def f(a, b):
		return a + b
	return eval(f, args)


def sub(*args):
	def f(a, b):
		return a - b
	return eval(f, args)


def mul(*args):
	def f(a, b):
		return a * b
	return eval(f, args)


def truediv(*args):
	def f(a, b):
		return a / b
	return eval(f, args)


def floordiv(*args):
	def f(a, b):
		return a // b
	return eval(f, args)


def mod(*args):
	def f(a, b):
		return a % b
	return eval(f, args)


# noinspection PyShadowingBuiltins
def pow(*args, modulo=None):
	def f(a, b):
		return a ** b
	if modulo is not None:
		raise NotImplemented("! modulo on power op not implemented")
	return eval(f, args)


def xnd(*args):
	def f(a, b):
		return a & b
	return eval(f, args)


def xr(*args):
	def f(a, b):
		return a | b
	return eval(f, args)


def xor(*args):
	def f(a, b):
		return a ^ b
	return eval(f, args)


def inv(*args):
	def f(a):
		return ~a
	return f(*args)


def lshift(*args):
	def f(a, b):
		return a << b
	return eval(f, args)


def rshift(*args):
	def f(a, b):
		return a >> b
	return eval(f, args)
