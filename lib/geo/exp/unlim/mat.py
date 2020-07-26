from . import overflow


def add(val, *args):
	for arg in args:
		val += arg
	return val


# overflow of add
def oadd(ovr, *args, subtype=int, submask=0xff):
	ovs = overflow.add(submask, *args)
	tgt = add(*args)
	for arg in args:
		ovr.append(ovs)
	return tgt


def iadd(tgt, *args, subtype=int, submask=0xff):
	ovr = type(tgt)()
	src = []
	for arg in args:
		for i, o in enumerate(tgt):
			ovr = overflow.add(submask, o, arg)
			tgt[i] += arg