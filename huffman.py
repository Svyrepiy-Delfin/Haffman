from functools import reduce

operation, input_name, output_name = map(str, input().split())
with open(input_name, 'r', encoding="utf-8") as f:
    text = f.readlines()


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
    hufman_tree(root, "", alphabet)
    return alphabet


def huffman_tree_decode(text, zeros_number):
    length = int(text[1])
    chars = {}
    for i in range(2, length + 2):
        string = text[i]
        if string[0] == ":":
            chars[":"] = int(string[3])
        else:
            chars[string.split(":")[0]] = int(string.split(":")[1])
    code = decompression(text[length + 2], zeros_number)
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
    dictionary = str(len(alphabet.keys())) + "\n"
    for ch in chars:
        if str(ch) != "\n":
            dictionary = dictionary + str(ch) + ": " + str(chars[ch]) + "\n"
        else:
            dictionary = dictionary + "\\n" + ": " + str(chars[ch]) + "\n"
    return dictionary, code


def hufman_tree(root, str, alphabet):
    if root.ch != "":
        alphabet[root.ch] = str
        return

    hufman_tree(root.right, str + '1', alphabet)
    hufman_tree(root.left, str + '0', alphabet)

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


def compression(binary_code):
    byte_code = ""
    bins = ""
    zeros_number = 7 - len(binary_code) % 7
    binary_code = "0" * zeros_number + binary_code
    for bit in binary_code:
        bins += bit
        if len(bins) == 7:
            if chr(int(bins)) != "\n":
                byte_code += chr(int(bins))
            else:
                byte_code += "\\n"
            bins = ""
    return byte_code, zeros_number


def decompression(byte_code, zeros_number):
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
        buff = "0" * (7 - len(buff)) + buff
        binary_code += buff
    return binary_code[zeros_number:]



if operation == "--encode":
    encoding_text = reduce(lambda x, y: x + y, text)
    dictionary, binary = huffman_tree_encode(encoding_text)

    byte_code, zeros_number = compression(binary)

    f = open(output_name, "w", encoding="utf-8")
    f.write(chr(zeros_number) + '\n')
    f.write(dictionary)
    f.write(byte_code)
    f.close()
elif operation == "--decode":
    zeros_number = int(ord(text[0][:1]))
    actual_text = huffman_tree_decode(text, zeros_number)
    f = open(output_name, "w")
    f.write(actual_text)

with open("test1.txt", "w", encoding="utf-8") as f:
    f.write("abcdfd")
with open("test2.txt", "w", encoding="utf-8") as f:
    f.write("󶥑􏏙𛆘✛􌴷")