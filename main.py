operation, input_name, output_name = map(str, input().split())
with open(input_name) as f:
    text = f.readline()


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


def huffman_tree(text):
    chars = {}
    for i in range(len(text)):
        ch = text[i]
        if ch in chars.keys():
            chars[ch] += 1
        else:
            chars[ch] = 1

    chars = dict(sorted(chars.items(), key=lambda item: item[1]))
    queue = []
    for ch in chars:
        queue.append(Node(ch, chars[ch], None, None))

    while len(queue) != 1:
        left = queue[0]
        right = queue[1]

        queue.remove(left)
        queue.remove(right)

        freq_sum = right.freq + left.freq
        queue.append(Node('', freq_sum, left, right))

        queue.sort()

    root = queue[0]
    alphabet = {}
    for ch in chars.keys():
        alphabet[ch] = ""
    encode(root, "", alphabet)
    code = text_encode(alphabet, text)
    print(code)
    print(decode(code, root))




def encode(root, str, alphabet):
    if root.ch != "":
        alphabet[root.ch] = str
        return

    encode(root.right, str + '1', alphabet)
    encode(root.left, str + '0', alphabet)

    return

def text_encode(alphabet, text):
    code = ''
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


huffman_tree(text)
