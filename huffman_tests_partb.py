import unittest
from huffman import *

class TestList(unittest.TestCase):
    def test_parse_header_01(self):
        header = "97 2 98 4 99 8 100 16 102 2"
        freqlist = parse_header(header)
        anslist = [0]*256
        anslist[97:104] = [2, 4, 8, 16, 0, 2, 0] 
        self.assertListEqual(freqlist[97:104], anslist[97:104])

    def test_parse_header(self):
        header = " "
        freq_list = parse_header(header)
        answer_list = [0] * 256
        self.assertListEqual(freq_list,answer_list)
    
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