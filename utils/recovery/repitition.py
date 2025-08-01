def repetition_encode(bitstring): return [''.join(bit * 3 for bit in bitstring), 0, 0]


def repetition_decode(codeword, a, b):
	decoded = ''
	for i in range(0, len(codeword), 3):
		chunk = codeword[i:i+3]
		decoded += '1' if chunk.count('1') > chunk.count('0') else '0'
	return decoded




