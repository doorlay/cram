import unittest
from huffman import *

class TestList(unittest.TestCase):

    def test_create_code(self):
        freqlist = cnt_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
        codes = create_code(hufftree)
        self.assertEqual(codes[ord('d')], '1')
        self.assertEqual(codes[ord('a')], '0000')
        self.assertEqual(codes[ord('f')], '0001')

    def test_comes_before(self):
        one = HuffmanNode(100,10)
        two = HuffmanNode(80,1)
        self.assertTrue(comes_before(two,one))
        three = HuffmanNode(80,5)
        self.assertTrue(comes_before(two,three))
        four = HuffmanNode(77,5)
        self.assertTrue(comes_before(four,three))

    def test_combine(self):
        one = HuffmanNode(100,10)
        two = HuffmanNode(80,3)
        sum12 = HuffmanNode(80,13)
        sum12.left = two
        sum12.right = one
        self.assertEqual(combine(one,two),sum12)

# Compare files - takes care of CR/LF, LF issues
def compare_files(file1,file2):
    match = True
    done = False
    with open(file1, "r") as f1:
        with open(file2, "r") as f2:
            while not done:
                line1 = f1.readline().strip()
                line2 = f2.readline().strip()
                if line1 == '' and line2 == '':
                    done = True
                if line1 != line2:
                    done = True
                    match = False
    return match

if __name__ == '__main__': 
   unittest.main()