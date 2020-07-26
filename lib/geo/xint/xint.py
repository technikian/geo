from random import randint
from copy import deepcopy
from core.object import Conditional, Operable

# note: doing add/sub with twos compliment would require both


# noinspection PyShadowingBuiltins
# this is a deliberate overload, don't remove it without finding out what it does!
def next(iterator, default):
	try:
		r = iterator.__next__()
	except StopIteration:
		r = default
	return r


def nojump_min(a, b):
	return b ^ ((a ^ b) & -(a < b))


def jump_min(a, b):
	return a if a < b else b


def nojump_max(a, b):
	return a ^ ((a ^ b) & -(a < b))


def jump_max(a, b):
	return a if a > b else b


class XList:
	def yeet(self, *args, **kwargs):
		raise AttributeError("! super attribute depreciated")

	def append(self, *args):
		self.yeet(*args)

	def clear(self, *args):
		self.yeet(*args)

	def copy(self, *args):
		self.yeet(*args)

	def count(self, *args):
		self.yeet(*args)

	def extend(self, *args):
		self.yeet(*args)

	def index(self, *args):
		self.yeet(*args)

	def insert(self, *args):
		self.yeet(*args)

	def pop(self, *args):
		self.yeet(*args)

	def remove(self, *args):
		self.yeet(*args)

	def reverse(self, *args):
		self.yeet(*args)

	def sort(self, *args):
		self.yeet(*args)

	@property
	def default(self):
		return self._default

	@default.setter
	def default(self, x):
		self._default = 0xff if x else 0x00

	def __init__(self, iterable=(), *, default=0x00):
		self.data = []
		self.default = default
		for i, o in zip(range(iterable.__len__()), iterable):
			self.data.append(o & 0xff)

	def __getitem__(self, item):
		try:
			return self.data.__getitem__(item)
		except IndexError:
			return self.default

	def __setitem__(self, key, value):
		value &= 0xff
		self.data.__setitem__(key, value)

	def __len__(self):
		return self.data.__len__()

	def resize(self, length):
		if length <= 0:
			raise ValueError("! length should be > 0")
		while len(self.data) > length:
			self.data.pop(-1)
		while len(self.data) < length:
			self.data.append(self.default)


class XInt(Conditional, Operable):
	@property
	def sign(self):
		return self.data.default

	@classmethod
	def from_rand(cls, length):
		r = XInt(0)
		r.data.resize(length)
		for i in range(length):
			r.data[i] = randint(0, 255)
		r.data.default = randint(0, 1)
		return r

	def __init__(self, x):
		if isinstance(x, XInt):
			self.data = XList(x.data, default=x.data.default)
			return
		x = int(x)
		r = []
		for i in range((x.bit_length() + 7) // 8):
			r.append(x)
			x >>= 8
		self.data = XList(r, default=-1 if x < 0 else 0)

	def __int__(self):
		if self.sign:
			r = 0
			for i, x in zip(range(len(self.data)), self.data):
				r |= (~x & 0xff) << (i * 8)
			r = ~r
		else:
			r = 0
			for i, x in zip(range(len(self.data)), self.data):
				r |= (x & 0xff) << (i * 8)
		return r

	def __str__(self):
		return "{}".format(int(self))

	def __repr__(self):
		# print(self.data)
		return "XInt({})".format(int(self))

	def __len__(self):
		return len(self.data)

	def __neg__(self):
		r = ~deepcopy(self)
		r += 1
		return r

	def __eq__(self, other):
		return self._eq_(other)

	def __lt__(self, other):
		return self._lt_(other)

	def __iadd__(self, other):
		return self._iadd_(other)

	def __isub__(self, other):
		return self._iadd_(-other)

	def _lt_(self, other):
		if self.data.default < other.times.default:
			return False
		if self.data.default > other.times.default:
			return True
		r = bool(self.data.default)
		i = max(len(self), len(other))
		while i:
			i -= 1
			if self.data[i] < other.times[i]:
				return not r
		return r

	def _eq_(self, other):
		limit = max(len(self), len(other))
		for a, b, i in zip(self.data, other.times, range(limit)):
			del i
			if a != b:
				return False
		return True

	def _iinv_(self):
		self.data.default = ~self.data.default
		for i, x in zip(range(len(self)), self.data):
			self.data[i] = ~x

	def _iadd_(self, other):
		other = other if isinstance(other, XInt) else XInt(other)
		limit = max(len(self), len(other))
		self.data.resize(limit)

		# setup a loop
		i = 0
		c = 0
		overflow = False
		for a, b in zip(self.data, other.data):

			# calculation sequence - work out the value for byte[i] in data array
			r = c  # start with overflow from last cycle
			# c = 0  # initialize overflow for this cycle
			r = (r + a) & 0xff  # add array byte from self
			c = r < a  # check for overflow
			r = (r + b) & 0xff  # add array byte from other
			c |= r < b  # check for overflow
			self.data[i] = r  # store result

			# flow control
			i += 1
			if i != limit:
				continue

			# check for overflow on last data byte (overflow for negative ints is reversed)
			if not overflow and c != self.data.default & 1:
				overflow = True
				limit += 1
				self.data.resize(limit)
				continue  # make more space, and go around again

			break

		# calculate the sign
		self.data.default = (self.data.default + other.data.default + c) & 1
		return self

	# todo mul, div, mod, pow


def bits(count=16):
	if count < 1:
		raise ValueError("! need value > 0")
	count -= 1
	r = 1
	while count:
		r |= r << 1
		count -= 1
	return r


#  -153 65500 XInt(-153) XInt(65500) 65347 XInt(-189)
#  65410 65486 XInt(65410) XInt(65486) 130896 XInt(65360)
#  65517 65328 XInt(65517) XInt(65328) 130845 XInt(65309)


def test_1(count):
	good = True
	bit_count = 128
	for i in range(count):
		x = randint(~bits(bit_count), bits(bit_count))
		y = XInt(x)
		r = int(x) == int(y)
		if not r:
			print("! {} {}".format(x, y))
			good = False
	print("test_1 {}".format("passed" if good else "failed"))


def test_2(count, bit_count=128, print_good=False):
	good = True
	# bit_count = 1024 * 128
	for i in range(count):
		x, y = (randint(~bits(bit_count), bits(bit_count)), randint(-bits(bit_count), bits(bit_count)))
		a, b = (XInt(x), XInt(y))
		z = x + y
		c = XInt(a)  # copy constructs
		c += b
		r = z == int(c)
		if not r:
			print("! {} {} {} {} {} {}".format(x, y, a, b, z, c))
			good = False
		elif print_good:
			print(". {} + {} = {}".format(x, y, z))
	print("test_2 {}".format("passed" if good else "failed"))


# todo test == and <


if __name__ == "__main__":

	# tests = (
	# 	XInt(-99),
	# 	XInt(99) + 100,  # 99 + 100 = 199
	# 	XInt(0xf) - 0xf - 1,  # 15 - 16 = -1
	# 	XInt(-153) + 65500,  # 65347
	# 	XInt(65410) + 65486,  # 130896
	# 	XInt(65517) + 65328,  # 130845
	# )

	# for test in tests:
	# 	print(test)

	# a = XInt.from_rand(1024*128)
	# print(a)
	# print(" + ")
	# b = XInt.from_rand(1024*128)
	# print(b)
	# print(" = ")
	# c = a + b
	# print(c)
	# print(" ")

	# test_1(10000)
	test_2(10000, 1024 * 1, 0)
	# total = 100.0
#
	# for i in range(8):
#
	# 	start = time.perf_counter()
#
	# 	for i in range(5000000):
	# 		max(randint(0, 0xffffffff), randint(0, 0xffffffff))
#
	# 	stop = time.perf_counter()
	# 	total = stop - start if stop - start < total else total
#
	# 	print(total)

	# undo marker!  3.27
