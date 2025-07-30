def elias_gamma_encode(n):
    """Encode integer n ≥ 1 using Elias gamma coding."""
    binary = bin(n)[2:]
    offset = binary[1:]  # remove leading 1
    length = len(offset)
    return '0' * length + binary

def elias_gamma_decode(bits, i):
    """Decode Elias gamma code starting at index i. Returns (value, next_index)."""
    zeros = 0
    while i < len(bits) and bits[i] == '0':
        zeros += 1
        i += 1
    if i + zeros >= len(bits): raise ValueError("Incomplete Elias code.")
    binary = '1' + bits[i+1:i+1+zeros]
    return int(binary, 2), i + 1 + zeros

def lempel_ziv_encoding(raw_text):
    dict_index = 1
    encoding = {}
    text = list(raw_text)
    output_bits = ""

    # First character is always new
    encoding[text[0]] = dict_index
    dict_index += 1
    output_bits += elias_gamma_encode(1) + '0' + text[0]

    i = 1
    while i < len(text):
        char = text[i]
        if char in encoding:
            string = char
            j = i + 1
            while j < len(text) and string in encoding:
                string += text[j]
                j += 1

            if string not in encoding:
                prefix = string[:-1]
                new_char = string[-1]
                index = encoding[prefix]
                output_bits += elias_gamma_encode(index) + new_char
                encoding[string] = dict_index
                dict_index += 1
            else:
                index = encoding[string]
                output_bits += elias_gamma_encode(index)  # No new char
                # (won’t actually happen due to how LZ works)
        else:
            output_bits += elias_gamma_encode(1) + '0' + char
            encoding[char] = dict_index
            dict_index += 1
            j = i + 1
        i = j
    return [output_bits, 0]


def lempel_ziv_decoding(bitstring, a):
    decoding = {}
    decoded_output = ""
    i = 0
    dict_index = 1

    while i < len(bitstring):
        index, i = elias_gamma_decode(bitstring, i)
        if i >= len(bitstring): break  # Malformed

        symbol = bitstring[i]
        i += 1

        if index == 1 and symbol == '0':
            # Raw char
            char = bitstring[i]
            i += 1
            decoded_output += char
            decoding[dict_index] = char
        else:
            prev_string = decoding.get(index)
            if prev_string is None:
                raise ValueError(f"Invalid dictionary index {index}")
            string = prev_string + symbol
            decoded_output += string
            decoding[dict_index] = string

        dict_index += 1

    return decoded_output
