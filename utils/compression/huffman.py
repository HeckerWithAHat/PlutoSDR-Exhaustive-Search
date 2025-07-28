class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
def huffman_encoding(text):
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
    return encoded_text, root
def huffman_decoding(encoded_text, root):
    decoded_text = ""
    node = root
    for bit in encoded_text:
        if bit == "0":
            node = node.left
        else:
            node = node.right
        if node.char is not None:
            decoded_text += node.char
            node = root
    return decoded_text