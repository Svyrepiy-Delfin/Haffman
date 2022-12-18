from functools import reduce

operation, input_name, output_name = map(str, input().split())
with open(input_name, 'r', encoding="utf-8") as f:
    text = f.readlines()

CHARCODE = 4

class Node:
    ch = ''
    freq = 0
    left = None
    right = None

    def __lt__(self, other):
        return self.freq < other.freq

    def __init__(self, ch, freq, left, right):
        self.ch = ch
        self.freq = freq
        self.left = left
        self.right = right


def huffman_tree_builder(chars):
    chars = dict(sorted(chars.items(), key=lambda item: item[1]))
    queue = []
    for ch in chars:
        queue.append(Node(ch, chars[ch], None, None))

    while len(queue) != 1:
        left = queue[0]
        right = queue[1]

        queue.remove(queue[0])
        queue.remove(queue[0])

        freq_sum = right.freq + left.freq
        queue.append(Node('', freq_sum, left, right))

        queue.sort()

    root = queue[0]
    alphabet = {}
    for ch in chars.keys():
        alphabet[ch] = ""
    huffman_tree(root, "", alphabet)
    return alphabet


def huffman_tree_decode(text, zeros_num_byte, zeros_num_char):
    length = ord(text[2][0])
    chars = {}
    for i in range(3, length + 3):
        string = text[i]
        if string[0] == ":":
            chars[":"] = int(dict_decompression(string[3]))
        else:
            chars[string.split(":")[0]] = int(dict_decompression(string.split(":")[1]))
    byte_code = char_decompression(text[length + 3], zeros_num_char)
    code = byte_decompression(byte_code, zeros_num_byte)


    alphabet = huffman_tree_builder(chars)
    char_code = ""
    actual_text = ""
    for i in code:
        char_code += i
        if char_code in alphabet.values():
            if list(alphabet.keys())[list(alphabet.values()).index(char_code)] == "\\n":
                actual_text += "\n"
            else:
                actual_text += list(alphabet.keys())[list(alphabet.values()).index(char_code)]
            char_code = ""
    return actual_text


def huffman_tree_encode(text):
    chars = {}
    for i in range(len(text)):
        ch = text[i]
        if ch in chars.keys():
            chars[ch] += 1
        else:
            chars[ch] = 1

    alphabet = huffman_tree_builder(chars)
    code = encode(alphabet, text)
    dictionary = chr(len(alphabet.keys())) + "\n"
    for ch in chars:
        if str(ch) != "\n":
            dictionary = dictionary + str(ch) + ":" + dict_compression(str(chars[ch])) + "\n"
        else:
            dictionary = dictionary + "\\n" + ":" + dict_compression(str(chars[ch])) + "\n"
    return dictionary, code


def huffman_tree(root, str, alphabet):
    if root.ch != "":
        alphabet[root.ch] = str
        return

    huffman_tree(root.right, str + '1', alphabet)
    huffman_tree(root.left, str + '0', alphabet)

    return


def encode(alphabet, text):
    code = ""
    for ch in text:
        code += alphabet[ch]
    return code


def decode(code, root):
    current_root = root
    text = ""
    for i in code:
        if i == '0':
            current_root = current_root.left
        else:
            current_root = current_root.right
        if current_root.ch != "":
            text += current_root.ch
            current_root = root
    return text


def byte_compression(binary_code):
    byte_code = ""
    triplet = ""
    if len(binary_code) % 3 == 0:
        zeros_num = 0
    else:
        zeros_num = 3 - len(binary_code) % 3
    binary_code = "0" * zeros_num + binary_code
    for digit in binary_code:
        triplet += digit
        if len(triplet) == 3:
            byte_code += str(int(triplet, 2))
            triplet = ""
    return byte_code, zeros_num

def byte_decompression(byte_code, zeros_num):
    binary = ""
    for byte in byte_code:
        buff = bin(int(byte))[2:]
        binary += "0" * (3 - len(buff)) + buff
    return binary[zeros_num:]

def char_compression(binary_code):
    byte_code = ""
    bins = ""
    if len(binary_code) % CHARCODE == 0:
        zeros_number = 0
    else:
        zeros_number = CHARCODE - len(binary_code) % CHARCODE
    binary_code = "0" * zeros_number + binary_code
    for bit in binary_code:
        bins += bit
        if len(bins) == CHARCODE:
            if chr(int(bins)) != "\n":
                byte_code += chr(int(bins))
            else:
                byte_code += "\\n"
            bins = ""
    return byte_code, zeros_number


def char_decompression(byte_code, zeros_number):
    binary_code = ""
    isN = False
    for byte in byte_code:
        if isN:
            isN = False
            continue
        if byte == "\\" and byte_code[byte_code.index(byte) + 1] == "n":
            byte = "\n"
            isN = True
        buff = str(ord(byte))
        buff = "0" * (CHARCODE - len(buff)) + buff
        binary_code += buff
    return binary_code[zeros_number:]

def dict_compression(value):
    char_code = ""
    byte = ""
    if len(value) % 6 != 0:
        value = "0" * (6 - len(value) % 6) + value
    for digit in value:
        byte += digit
        if len(byte) == 6:
            if chr(int(byte)) != "\n":
                char_code += chr(int(byte))
            else:
                char_code += "\\n"
            byte = ""
    return char_code

def dict_decompression(char_code):
    value = ""
    isN = False
    zeros_number = 0
    for byte in char_code:
        if isN:
            isN = False
            continue
        if byte == "\\" and char_code[char_code.index(byte) + 1] == "n":
            byte = "\n"
            isN = True
        buff = str(ord(byte))
        buff = "0" * (6 - len(buff)) + buff
        value += buff
    i = 0
    while value[i] == "0":
        zeros_number += 1
        i += 1
    return value[zeros_number:]


if operation == "--encode":
    encoding_text = reduce(lambda x, y: x + y, text)
    dictionary, binary = huffman_tree_encode(encoding_text)

    byte_code, zeros_num_byte = byte_compression(binary)
    char_code, zeros_num_char = char_compression(byte_code)

    f = open(output_name, "w", encoding="utf-8")
    f.write(chr(zeros_num_byte) + '\n')
    f.write(chr(zeros_num_char) + '\n')
    f.write(dictionary)
    f.write(char_code)
    f.close()
elif operation == "--decode":
    zeros_number_byte = int(ord(text[0][:1]))
    zeros_number_char = int(ord(text[1][:1]))
    actual_text = huffman_tree_decode(text, zeros_number_byte, zeros_number_char)
    f = open(output_name, "w", encoding="utf-8")
    f.write(actual_text)
