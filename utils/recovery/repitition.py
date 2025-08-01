def repetition_encode(bitstring): return [''.join(bit * 5 for bit in bitstring), 0, 0]


def repetition_decode(codeword, a, b):
	decoded = ''
	for i in range(0, len(codeword), 5):
		chunk = codeword[i:i+5]
		decoded += '1' if chunk.count('1') > chunk.count('0') else '0'
	return decoded




