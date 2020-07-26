import time
import random


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


def is_prime(x):
	if x in _prime:
		return True
	return False







def is_odd(x):
	# return x % 2
	return x & 1


fa = lambda x: x&1
fb = lambda x: x % 2


def time_test(func_a, func_b):
	a_time = 0
	b_time = 0
	for i in range(1000000):
		x = random.randint(0, 10000)

		temp = time.perf_counter()
		func_a(x)
		a_time += time.perf_counter() - temp

		temp = time.perf_counter()
		func_b(x)
		b_time += time.perf_counter() - temp
	return a_time, b_time




def modular_congruence(a, b, n):
	# return True if a % n == b % n else False
	return False if (a - b) % n else True  # this method appears marginally faster in python






for i in range(100):
	if i % 2 == 0:
		continue
	#if is_prime(i) and not (modular_congruence(i, 2, 5) or modular_congruence(i, -2, 5)):
	#	print(i, "bad")
	print(i, modular_congruence(i, 2, 5) or modular_congruence(i, -2, 5), is_prime(i))






# 6k +- 1 optimization
def simple(n):
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





# ===
#
# if and only if (both statements are true or both statements are false)
#
#
#
#

