import numpy as np
class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
def huffman_encoding(text):
    """
    Parameters:
        text - String to be encoded using Huffman coding
    """
    frequency = __import__('collections').Counter(text)
    nodes = [Node(char, freq) for char, freq in frequency.items()]
    while len(nodes) > 1:
        nodes.sort(key=lambda node: node.freq)
        left = nodes.pop(0)
        right = nodes.pop(0)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        nodes.append(merged)
    while len(nodes) > 1:
        nodes.sort(key=lambda node: node.freq)
    root = nodes[0] if nodes else None
    def generate_codes(node, current_code, codes):
        if node is None:
            return
        if node.char is not None:
            codes[node.char] = current_code
            return
        generate_codes(node.left, current_code + "0", codes)
        generate_codes(node.right, current_code + "1", codes)
    codes = {}
    generate_codes(root, "", codes)
    encoded_text = "".join(codes[char] for char in text)
    tree_bits = serialize_huffman_tree(root)
    return f"{len(tree_bits):016b}" + tree_bits + encoded_text
def huffman_decoding(encoded_text):
    tree_len = int(encoded_text[:16], 2)
    tree_bits = encoded_text[16:16+tree_len]
    compressed_bits = encoded_text[16+tree_len:]
    root = deserialize_huffman_tree(tree_bits)
    decoded_text = ""
    node = root
    for bit in compressed_bits:
        if bit == np.int64(0) or bit == '0':
            node = node.left
        else:
            node = node.right
        if node.char is not None:
            decoded_text += node.char
            node = root
    return decoded_text






def serialize_huffman_tree(node):
    if node is None:
        return ""
    if node.char is not None:
        return "1" + f"{ord(node.char):08b}"  # '1' + 8-bit char
    return "0" + serialize_huffman_tree(node.left) + serialize_huffman_tree(node.right)



def deserialize_huffman_tree(bitstream):
    def helper(index):
        if bitstream[index] == '1':
            char_bits = bitstream[index+1:index+9]
            char = chr(int(char_bits, 2))
            return Node(char, 0), index + 9
        else:
            left, next_index = helper(index + 1)
            right, final_index = helper(next_index)
            node = Node(None, 0)
            node.left = left
            node.right = right
            return node, final_index
    root, _ = helper(0)
    return root