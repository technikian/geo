
from time import perf_counter
from random import randint


class Task:
	def __init__(self, f, *args, **kwargs):
		self.function = f
		self.args = args
		self.kwargs = kwargs

	def exec(self):
		return self.function(*self.args, **self.kwargs)


def perf_test(task):
	initial = perf_counter()
	task.exec()
	final = perf_counter()
	return final - initial


def add(vector_a, vector_b, t):
	return t(a + b for a, b in zip(vector_a, vector_b))


def iadd(tgt_vector, vector):
	for i, v in zip(range(len(tgt_vector)), vector):
		tgt_vector[i] += v
	return tgt_vector


def iadd_copy(vector_a, vector):
	from copy import deepcopy
	tgt_vector = deepcopy(vector_a)
	for i, v in zip(range(len(tgt_vector)), vector):
		tgt_vector[i] += v
	return tgt_vector


def add_2(vector_a, vector_b, t):
	return t(vector_a[i] + vector_a[i] for i in range(min(len(vector_a), len(vector_b))))


def sub(vector_a, vector_b, t):
	return t(a - b for a, b in zip(vector_a, vector_b))


def mul(vector, value, t):
	return t(v * value for v in vector)


class W:
	def __init__(self, value):
		self.value = value


class Test:
	class Iter:
		def __init__(self, parent):
			self.parent = parent
			self._m_iter = iter(parent.values)

		def __next__(self):
			return next(self._m_iter).value

	def __init__(self, values):
		self.values = tuple(W(v) for v in values)

	def __iter__(self):
		return Test.Iter(self)

	def __len__(self):
		return len(self.values)

	def __getitem__(self, item):
		return self.values[item].value

	def __setitem__(self, key, value):
		self.values[key].value = value


sample_a = list(randint(0, 10000) for i in range(500000))
sample_b = list(randint(0, 10000) for j in range(500000))
t_sample_a = Test(sample_a)
t_sample_b = Test(sample_b)


def one_call(x):
	return x + 1


def two_call(x):
	return one_call(x)


def one_call_test(values):
	return tuple(one_call(v) for v in values)


def two_call_test(values):
	return tuple(two_call(v) for v in values)


tasks = (
	Task(add, tuple(sample_a), tuple(sample_b), tuple),
	Task(add, sample_a, sample_b, list),
	Task(add_2, sample_a, sample_b, list),
	Task(iadd_copy, sample_a, sample_b),
	Task(iadd, sample_a, sample_b),
	Task(add, t_sample_a, t_sample_b, Test),
	Task(add_2, t_sample_a, t_sample_b, Test),
	Task(iadd_copy, t_sample_a, t_sample_b),
	Task(iadd, t_sample_a, t_sample_b),
	Task(one_call_test, t_sample_b),
	Task(two_call_test, t_sample_b),
)


for tsk in tasks:
	print(perf_test(tsk))


# findings:
# lists are faster than tuples of wrappers
# iadd is faster than add for lists and tuples of wrappers
# tuples are faster than lists (to add all elements to a new iterable), but not by much
# iadd to list is faster than add to new tuple
# nested function calls are slower than non-nested
# defining add by copying and using iadd is very, very slow


if __name__ == "__main__":
	pass
