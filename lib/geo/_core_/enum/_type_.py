
class Enum:
	@classmethod
	def from_set(cls, iterable=()):
		return cls(**{k: i for i, k in enumerate(iterable)})

	@classmethod
	def from_map(cls, mapping=None):
		if mapping is None:
			mapping = {}
		return cls(**mapping)

	def __init__(self, **params):
		self.params = params

	def __repr__(self):
		return f"Enum(**{repr(object.__getattribute__(self, 'params'))})"

	def __len__(self):
		return object.__getattribute__(self, 'params').__len__()

	def __iter__(self):
		return object.__getattribute__(self, 'params').__iter__()

	def __reversed__(self):
		return object.__getattribute__(self, 'params').__reversed__()

	def __getattribute__(self, item):
		return object.__getattribute__(self, "params")[item]

	def __lt__(self, other):
		raise NotImplementedError

	def __eq__(self, other):
		raise NotImplementedError


class Selector:
	class Setter:
		def __init__(self, parent):
			self.parent = parent

		def __getattribute__(self, item):
			def set_ret(selector, x):
				selector.value = x
				return x
			parent = object.__getattribute__(self, "parent")
			enum = parent.enum
			value = getattr(enum, item)
			# parent.value = value
			# this is why walrus was introduced: so this function could set and return parent.value
			# doing this way is kinda inefficient, but necessary for backwards compatibility and to
			# maintain that parent.value is set when the function is called, not when the attribute is getted
			return lambda: set_ret(parent, value)

	@property
	def get(self):
		return self.enum

	@property
	def set(self):
		return self._m_setter

	def __init__(self, enum, value=None):
		self.enum = enum  # may want to use same enum object multiple times, since enum is effectively immutable
		self.value = value
		self._m_setter = self.Setter(self)

	def __repr__(self):
		return f"Selector({repr((self.enum, self.value))[1:-1]})"

	def __lt__(self, other):
		try:
			return self.value < other.value
		except AttributeError:
			return self.value < other

	def __eq__(self, other):
		try:
			return self.value == other.value
		except AttributeError:
			return self.value == other
