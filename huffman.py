class HuffmanNode:
    def __init__(self, char_ascii, freq):
        self.char_ascii = char_ascii  # stored as an integer - the ASCII character code value
        self.freq = freq              # the frequency count associated with the node
        self.left = None              # Huffman tree (node) to the left
        self.right = None             # Huffman tree (node) to the right

    def __lt__(self, other):
        return comes_before(self, other) # Allows use of Python List sorting

    def __eq__(self,other):
        if type(self) == type(other) and \
            self.left == other.left and \
            self.right == other.right and \
            self.freq == other.freq and \
            self.char_ascii == other.char_ascii:
            return True
        else:
            return False

    def set_left(self, node):
        self.left = node

    def set_right(self, node):
        self.right = node

def comes_before(a, b):
    """Returns True if node a comes before node b, False otherwise"""

    if a.freq < b.freq:
        return True
    elif a.freq > b.freq:
        return False
    else:
        if a.char_ascii < b.char_ascii:
            return True
        else:
            return False

def combine(a, b):
    """Creates and returns a new Huffman node with children a and b, with the "lesser node" on the left
    The new node's frequency value will be the sum of the a and b frequencies
    The new node's char value will be the lesser of the a and b char ASCII values"""

    freq = a.freq + b.freq
    if a.char_ascii < b.char_ascii:
        char_ascii = a.char_ascii
    else:
        char_ascii = b.char_ascii
    newHuffNode = HuffmanNode(char_ascii,freq)
    if comes_before(a,b):
        newHuffNode.left = a
        newHuffNode.right = b
    else:
        newHuffNode.left = b
        newHuffNode.right = a
    return newHuffNode


def cnt_freq(filename):
    """Opens a text file with a given file name (passed as a string) and counts the 
    frequency of occurrences of all the characters within that file
    Returns a Python List with 256 entries - counts are initialized to zero.
    The ASCII value of the characters are used to index into this list for the frequency counts"""

    lst = [0 for x in range(256)]
    input_file = open(filename,"r")
    for line in input_file:
        for character in line:
            lst[ord(character)] += 1
    input_file.close()
    return lst

def create_huff_tree(freq_list):
    """Input is the list of frequencies (provided by cnt_freq()).
    Create a Huffman tree for characters with non-zero frequency
    Returns the root node of the Huffman tree. Returns None if all counts are zero."""

    new_lst = []
    for i in range(len(freq_list)):
        new_huff = HuffmanNode(i,freq_list[i])
        new_lst.append(new_huff)
    i = 0
    while True:
        if i == len(new_lst):
            break
        if new_lst[i].freq == 0:
            new_lst.pop(i)
        else:
            i += 1
    new_lst.sort(key = lambda x: x.freq)
    while len(new_lst) != 1:
        node_one = new_lst.pop(0)
        node_two = new_lst.pop(0)
        newNode = combine(node_one,node_two)
        if len(new_lst) == 0:
            new_lst.append(newNode)
            break
        for i in range(len(new_lst)):
            if i == len(new_lst) - 1:
                if comes_before(newNode,new_lst[i]):
                    new_lst.insert(i,newNode)
                else:
                    new_lst.append(newNode)
            elif comes_before(newNode,new_lst[i]):
                new_lst.insert(i,newNode)
                break
    return new_lst[0]

def create_code(node):
    """Returns an array (Python list) of Huffman codes. For each character, use the integer ASCII representation 
    as the index into the arrary, with the resulting Huffman code for that character stored at that location.
    Characters that are unused should have an empty string at that location"""
    code_list = [""] * 256
    code_path = []
    create_code_helper(node,code_path,code_list)
    return code_list

def create_code_helper(node,code_path,code_list):
    """
    Function to help create_code run recursively

    Parameters:
    node: A node of the huffman tree
    code_path: The path for the current node
    code_list: a list of huffman codes

    Returns:
    """
    if node.left is not None:
        code_path.append(str(0))
        create_code_helper(node.left,code_path,code_list)
    if node.right is not None:
        code_path.append(str(1))
        create_code_helper(node.right,code_path,code_list)
    if node.left is None and node.right is None:
        code = ""
        code_list[node.char_ascii] = code.join(code_path)
        code_path.pop(len(code_path)-1)
    else:
        if len(code_path) != 0:
            code_path.pop(len(code_path)-1)

def create_header(freq_list):
    """Input is the list of frequencies (provided by cnt_freq()).
    Creates and returns a header for the output file
    Example: For the frequency list asscoaied with "aaabbbbcc, would return “97 3 98 4 99 2” """

    new_lst = []
    for i in range(len(freq_list)):
        if freq_list[i] != 0:
            new_lst.append(str(i))
            new_lst.append(str(freq_list[i]))
    return_value = " "
    return return_value.join(new_lst)

def huffman_encode(in_file, out_file):
    """Takes inout file name and output file name as parameters
    Uses the Huffman coding process on the text from the input file and writes encoded text to output file
    Take not of special cases - empty file and file with only one unique character"""

    output_file = open(out_file,"w", newline = "")
    input_file = open(in_file,"r")
    flag = False
    for line in input_file:
        if line != "":
            flag = True
    input_file.close()
    input_file = open(in_file, "r")
    if flag == True:
        freq_list = cnt_freq(in_file)
        two_count = 0
        for number in freq_list:
            if number != 0:
                two_count += 1
        if two_count > 1:
            huffman_tree = create_huff_tree(freq_list)
            code_list = create_code(huffman_tree)
            output_file.write(create_header(freq_list))
            output_file.write("\n")
            for line in input_file:
                for character in line:
                    output_file.write("{}".format(code_list[ord(character)]))
        else:
            output_file.write(create_header(freq_list))

def parse_header(header_string):
    """
    takes a string input parameter (the first line of the
    input file) and returns a list of frequencies.

    Parameters:
    header_string: str containing the header infromation of the encoded file

    Returns:
    freq_list: lst containing the frequency of each character mapped to its ASCII value

    """

    freq_list = [0 for x in range(256)]
    header_list = header_string.split()
    for i in range(0,len(header_list),2):
        freq_list[int(header_list[i])] = int(header_list[i+1])
    return freq_list


def huffman_decode(encoded_file, decoded_file):
    """
    reads an encoded text file, encoded_file, and writes the decoded text into an 
    output text file, decode_file, using the Huffman Tree produced by using the header information

    Parameters:
    encoded_file = encoded input .txt file that we then decode
    decoded_file = output .txt file that has been decoded

    Returns:
    None

    """

    input_file = open(encoded_file,"r")
    output_file = open(decoded_file, "w", newline = "")
    header = input_file.readline()
    input_file.close()
    input_file = open(encoded_file, "r")
    flag = False
    for line in input_file:
        if line != "":
            flag = True
    input_file.close()
    if flag == True:
        freq_list = parse_header(header)
        huffman_tree = create_huff_tree(freq_list)
        input_file = open(encoded_file,"r")
        two_count = 0
        for number in freq_list:
            if number != 0:
                two_count += 1
        if two_count > 1:
            input_file.readline()
            encoded_data = input_file.readline()
            node = huffman_tree
            flag = False
            for bit in encoded_data:
                if bit == '0':
                    node = node.left
                    if node.left == None and node.right == None:
                        output_file.write(chr(node.char_ascii))
                        node = huffman_tree

                elif bit == '1':
                    node = node.right
                    if node.left == None and node.right == None:
                        output_file.write(chr(node.char_ascii))
                        node = huffman_tree
        else:
            ascii_value = 0
            num_times = 0
            for i in range(len(freq_list)):
                if freq_list[i] != 0:
                    ascii_value = i
                    num_times = freq_list[i]
            for x in range(num_times):
                output_file.write(chr(ascii_value))

huffman_encode("declaration.txt", "out.txt")