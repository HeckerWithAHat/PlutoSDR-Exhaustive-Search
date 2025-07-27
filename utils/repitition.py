def repetition_encode(bit, n): return [bit] * n

def repetition_decode(codeword, n): return 1 if sum(codeword) > n // 2 else 0
