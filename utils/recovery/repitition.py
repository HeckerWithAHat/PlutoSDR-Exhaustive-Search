def repetition_encode(bitstring, n=3): return ''.join(bit * n for bit in bitstring)


def repetition_decode(codeword, n=3):
	decoded = ''
	for i in range(0, len(codeword), n):
		chunk = codeword[i:i+n]
		decoded += '1' if chunk.count('1') > chunk.count('0') else '0'
	return decoded




