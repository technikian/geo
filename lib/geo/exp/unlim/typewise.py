

# left is +, right is -
def ishift(tgt, distance, *, subtype=type(None)):
	if distance > 0:
		while distance:
			tgt.insert(0, subtype())
			distance -= 1
	else:
		while distance:
			tgt.pop(0)
			distance += 1
	return tgt


def shift(src, distance, *, subtype=type(None)):
	tgt = type(src)(src)
	return ishift(tgt, distance, subtype=subtype)


