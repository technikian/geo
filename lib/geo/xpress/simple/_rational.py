# imports
# no imports
from random import randint


# the first 256 prime numbers
_prime = (
	2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53,
	59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131,
	137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223,
	227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311,
	313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409,
	419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503,
	509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613,
	617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719,
	727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827,
	829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941,
	947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049,
	1051, 1061, 1063, 1069, 1087, 1091, 1093, 1097, 1103, 1109, 1117, 1123, 1129, 1151, 1153, 1163,
	1171, 1181, 1187, 1193, 1201, 1213, 1217, 1223, 1229, 1231, 1237, 1249, 1259, 1277, 1279, 1283,
	1289, 1291, 1297, 1301, 1303, 1307, 1319, 1321, 1327, 1361, 1367, 1373, 1381, 1399, 1409, 1423,
	1427, 1429, 1433, 1439, 1447, 1451, 1453, 1459, 1471, 1481, 1483, 1487, 1489, 1493, 1499, 1511,
	1523, 1531, 1543, 1549, 1553, 1559, 1567, 1571, 1579, 1583, 1597, 1601, 1607, 1609, 1613, 1619
)


def is_prime(n):
	if n <= 3:
		return n > 1
	elif n % 2 == 0 or n % 3 == 0:
		return False
	i = 5
	while i * i <= n:
		if n % i == 0 or n % (i + 2) == 0:
			return False
		i = i + 6
	return True


def next_prime(n):
	n += 1
	while not is_prime(n):
		n += 1
	return n


def prime(n):
	l = len(_prime)
	if n < l:
		return _prime[n]

	i = l - 1
	p = _prime[i]
	while i != n:
		p = next_prime(p)
		i += 1

	return p


# least prime factor
def lpf(n):
	if n < 2:
		return 1
	p = 2  # first prime number
	while n % p:
		p = next_prime(p)
	return p


def prime_factors(n):
	r = []

	if n < 2:
		return r

	f = lpf(n)
	r.append(f)

	while not is_prime(n):
		n //= f
		f = lpf(n)
		r.append(f)

	return r


def gcf(a, b):
	a = prime_factors(a)
	b = prime_factors(b)
	c = []
	for f in a:
		i = 0
		while i < len(b):
			if f == b[i]:
				c.append(b.pop(i))
				break
			i += 1
	r = 1
	for f in c:
		r *= f
	return r


class Rational:
	@staticmethod
	def div(a, b):
		r = Rational(a.d * b.c, a.c * b.d)
		#r.simplify()
		return r

	@staticmethod
	def mul(a, b):
		r = Rational(a.d * b.d, a.c * b.c)
		#r.simplify()
		return r

	@staticmethod
	def add(a, b):
		if a.c == b.c:
			return Rational(a.d + b.d, a.c)
		r = Rational(a.d * b.c + b.d * a.c, a.c * b.c)
		#r.simplify()
		return r

	@staticmethod
	def sub(a, b):
		if a.c == b.c:
			return Rational(a.d - b.d, a.c)
		r = Rational(a.d * b.c - b.d * a.c, a.c * b.c)
		#r.simplify()
		return r

	@property
	def numerator(self):
		return self._numer

	@property
	def denominator(self):
		return self._denum

	@property
	def total(self):
		return self.r

	@property
	def a(self):
		if self.is_def:
			return self._numer // self._denum
		return 0

	@a.setter
	def a(self, value):
		self.d = int(value) * self.c + self.b

	@property
	def b(self):
		if self.is_def:
			return self._numer % self._denum
		return 0

	@b.setter
	def b(self, value):
		self.d = self.a * self.c + int(value)

	@property
	def c(self):
		return self._denum

	@c.setter
	def c(self, value):
		self._denum = int(value)

	@property
	def d(self):
		return self._numer

	@d.setter
	def d(self, value):
		self._numer = int(value)

	@property
	def r(self):
		return self._numer + self._denum

	@property
	def dc(self):
		return self.d, self.c

	@property
	def abc(self):
		return self.a, self.b, self.c

	@property
	def value(self):
		if self.is_def:
			return self._numer / self._denum
		return 0.0

	@property
	def is_def(self):
		return self._denum != 0

	@is_def.setter
	def is_def(self, value):
		if not value:
			self._numer = 0
			self._denum = 0
		elif not self.is_def:
			self._denum = 1

	@property
	def is_neg(self):
		if self._numer < 0:
			if self._denum < 0:
				return False
			return True
		if self._denum < 0:
			if self._numer < 0:
				return False
			return True
		return False

	@is_neg.setter
	def is_neg(self, value):
		if value:
			self._numer = -abs(self._numer)
		else:
			self._numer = abs(self._numer)
		self._denum = abs(self._denum)

	def __new__(cls, *args):
		if len(args) == 1 and isinstance(args[0], Rational):
			return args[0]
		o = super(Rational, cls).__new__(cls)
		# o._numer = 0
		# o._denum = 0
		return o

	def __init__(self, *args):
		if len(args) == 1 and isinstance(args[0], Rational):
			return

		# case switch
		if len(args) == 0:
			self.c = 0
			self.d = 0
			return
		if len(args) == 1:
			self.c = 1
			self.d = args[0]
			return
		if len(args) == 2:
			self.c = args[1]
			self.d = args[0]
			#self.simplify()
			return
		if len(args) == 3:
			self.c = args[2]
			self.b = args[1]
			self.a = args[0]
			#self.simplify()
			return

		# exception case
		text = []
		for a in args:
			text.append(a.__class__.__name__)
		raise TypeError(
			f"class {Rational.__name__} takes args "
			f"(), "
			f"({Rational.__name__}), "
			f"({int.__name__}), "
			f"({int.__name__}, {int.__name__}), "
			f"({int.__name__}, {int.__name__}, {int.__name__}), "
			f"received args "
			f"{tuple(text)}"
		)

	# not very efficient for large numbers
	def simplify(self):
		if self.is_def:
			neg = self.is_neg
			self.is_neg = False
			fac = gcf(self._numer, self._denum)
			self._numer //= fac
			self._denum //= fac
			self.is_neg = neg
			return
		self.is_def = False

	#
	# conversions
	#

	def __str__(self):
		# return f"{self._numer/self._denum}"
		return f"{self._numer}/{self._denum}"

	def __float__(self):
		return self.value

	#
	# comparisons
	#

	# ==
	def __eq__(self, other):
		return self.value.__eq__(float(other))

	# !=
	def __ne__(self, other):
		return self.value.__ne__(float(other))

	# >=
	def __ge__(self, other):
		return self.value.__ge__(float(other))

	# >
	def __gt__(self, other):
		return self.value.__gt__(float(other))

	# <=
	def __le__(self, other):
		return self.value.__le__(float(other))

	# <
	def __lt__(self, other):
		return self.value.__lt__(float(other))

	#
	# math
	#

	# -self
	def __neg__(self):
		return type(self)(self._numer.__neg__(), self._denum)

	# |self|
	def __abs__(self):
		return type(self)(self._numer.__abs__(), self._denum.__abs__())

	def __invert__(self):
		return type(self)(self._denum, self._numer)

	# /
	def __truediv__(self, other):
		return self.div(self, Rational(other))

	def __rtruediv__(self, other):
		return other.__truediv__(type(other)(self.value))

	def __itruediv__(self, other):
		other = Rational(other)
		self._numer *= other._denum
		self._denum *= other._numer
		return self

	# *
	def __mul__(self, other):
		return self.mul(self, Rational(other))

	def __rmul__(self, other):
		return other.__rmul__(type(other)(self.value))

	def __imul__(self, other):
		other = Rational(other)
		self._numer *= other._numer
		self._denum *= other._denum
		return self

	# +
	def __add__(self, other):
		return self.add(self, Rational(other))

	def __radd__(self, other):
		return other.__add__(type(other)(self.value))

	def __iadd__(self, other):
		result = self.add(self, Rational(other))
		self._numer = result._numer
		self._denum = result._denum
		return self

	# -
	def __sub__(self, other):
		return self.sub(self, Rational(other))

	def __rsub__(self, other):
		return other.__sub__(type(other)(self.value))

	def __isub__(self, other):
		result = self.sub(self, Rational(other))
		self._numer = result._numer
		self._denum = result._denum
		return self


_margin = 0.0000000001


def _test():
	c = randint(-1000, 1000)
	d = randint(-1000, 1000)
	e = randint(-1000, 1000)
	f = randint(-1000, 1000)
	v = d / c
	w = f / e
	x = Rational(d, c)
	y = Rational(f, e)

	# print(f"{c} {d} {e} {f}")

	i = v / w
	j = (x / y).value

	r = abs(i - j) > _margin
	if r:
		print(f"{i%j} {c} {d} {e} {f}")
	return r


def test(limit):
	for i in range(limit):
		if _test():
			print("fail")


# h = Rational(977, -701) * Rational(743, -98)
# print(h)
# h.simplify()
# print(h)


# test(1000)


