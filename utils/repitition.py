def repetition_encode(bit, n):
    """
    Encode bits using repetition code of length n.
    Example: bit=1, n=3 => [1,1,1]
    """
    return [bit] * n


def repetition_decode(codeword, n):
    """
    Decode bits by majority voting.
    """
    # Count the number of 1s in the codeword
    ones_count = sum(codeword)
    
    # If more than half are 1s, decode to 1; otherwise decode to 0
    if ones_count > n // 2:
        return 1
    else:
        return 0