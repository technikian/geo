
# useless because map exists
# def foreach(f, items):
# 	return (f(item) for item in items)


def sort(iterable, sortable_t=list):
	sortable = sortable_t(iterable)
	sortable.sort()
	return sortable


def accumulate(operator, iterable, default=None):
	"""repeatedly call function with args last_result, item. first call args is item[0], item[1]"""
	from inspect import signature as sig
	i = iter(iterable)
	try:
		r = next(i)
	except StopIteration:
		# raise ArithmeticError("! attempted arithmetic on 0 items")
		return default
	while True:
		try:
			item = next(i)
		except StopIteration:
			break
		try:
			r = operator(r, item)
		except TypeError as e:
			if len(sig(operator).parameters) != 2:
				raise TypeError("! operator function should take two arguments")
			raise e
	return r


def eq(*args):
	"""behavior for 0 or 1 arg not defined"""
	iterator = iter(args)
	try:
		a = next(iterator)
		b = next(iterator)
		while a == b:
			b = next(iterator)
	except StopIteration:
		return True
	return False


def cmp(*args):
	"""compares multiple iterables
	behavior for 0 or 1 arg not defined"""
	# todo this his horrible
	# print(cmp([1,2,3], [1,2,3], [1,2,3], [1,2,3,7], 1))
	# attempt to list the iterators
	try:
		iterators = tuple(map(iter, args))
	except TypeError:  # if not all items are iterable
		return eq(*args)  # do a regular equality check
	# compare items
	fails = 0
	while fails == 0:
		values = []
		for i in iterators:
			try:
				values.append(next(i))
			except StopIteration:
				fails += 1
		if not values:
			return True
		if not cmp(*values):
			return False
	return True if fails == len(args) else False


def add(*args):
	def pair(a, b):
		return a + b
	return accumulate(pair, args)


def sub(*args):
	def pair(a, b):
		return a - b
	return accumulate(pair, args)


def mul(*args):
	def pair(a, b):
		return a * b
	return accumulate(pair, args)


def div(*args):
	def pair(a, b):
		return a / b
	return accumulate(pair, args)


def mean(values):
	if not hasattr(values, "len"):  # generators have no len
		values = tuple(values)
	try:
		return add(*values) / len(values)
	except ArithmeticError:
		raise ZeroDivisionError("! attempted average of 0 items")


def variance(values, predefine_mean=None):
	average = mean(values) if predefine_mean is None else predefine_mean
	return add(*map(lambda x: (x - average) ** 2, values)) / len(values)


def stddev(values, predefine_mean=None):
	"""standard deviation"""
	from math import sqrt
	return sqrt(variance(values, predefine_mean=predefine_mean))
