

class NestedAdaptor:
	def __init__(self, nested_iterable):
		self.iterable = nested_iterable

	def __getitem__(self, item):
		r = self.iterable
		for k in item:
			r = r[k]
		return r

	def __setitem__(self, key, value):
		r = self.iterable
		for k in key[:-1]:
			r = r[k]
		r[key[-1]] = value
