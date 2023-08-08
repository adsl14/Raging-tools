def decompress_data(comp):

	decomp = b''
	pos = 0
	while pos < len(comp):

		value = comp[pos]
		pos += 1
		size = value >> 1

		if value & 1:
			offset = len(decomp) - comp[pos]
			pos += 1
			while size > 0:
				size -= 1
				decomp += decomp[offset].to_bytes(1, 'big')
				offset += 1
		else:
			while size > 0:
				size -= 1
				decomp += comp[pos].to_bytes(1, 'big')
				pos += 1

	return decomp
