import struct
import filecmp
import sys

# Compression and decompression functions for Huffman encoded files
# Assumes header line and encoded data are in files
# Doesn't handle the empty file and single unique character cases

def compress(input_file, output_file):
    i_f = open(input_file)
    header = i_f.readline()
    o_f = open(output_file, 'wb')
    o_f.write(bytes(header, 'utf8')) # preserve header as text
    code_string = i_f.readline() # read in code string
    i_f.close()
    n_bits = 0
    byte = 0
    for bit in code_string: # compress '0' and '1' chars into bytes
        byte = byte << 1
        n_bits += 1
        if bit == '1':
            byte += 1
        if n_bits == 8:
            o_f.write(struct.pack('B', byte)) # byte full, write to output
            byte = 0
            n_bits = 0
    if n_bits > 0: # last byte of compressed file used to indicate valid bits of last data byte
        o_f.write(struct.pack('B', byte)) # output the last data byte
        o_f.write(struct.pack('B', n_bits)) # use only n_bits of last data byte
    else: # last data byte is full
        o_f.write(struct.pack('B', 8)) #  use all 8 bits of last data byte

    o_f.close()

def decompress(input_file, output_file):
    i_f = open(input_file, "rb")
    o_f = open(output_file, 'w', newline='')
    c = 0
    while c != 0x0A:        # read in header text, write to output file
        c = struct.unpack('B', i_f.read(1))[0]
        o_f.write(chr(int(c)))
    data = i_f.read()
    i_f.close()
    for byte in data[0:len(data)-2]: # pull apart each data byte, except for last
        outstring = ""
        for i in range(8):
            if byte % 2 == 1:
                outstring = '1' + outstring
            else:
                outstring = '0' + outstring
            byte = byte >> 1
        o_f.write(outstring) # write string of '0' and '1' chars to output

    byte = data[len(data)-2] # last data byte
    outstring = ""
    for i in range(data[len(data)-1]): # number of valid bits in last data byte
        if byte % 2 == 1:
            outstring = '1' + outstring
        else:
            outstring = '0' + outstring
        byte = byte >> 1
    o_f.write(outstring)
    o_f.close()

if __name__ == '__main__': 
    if sys.argv[1] == '-c':
        compress(sys.argv[2], sys.argv[2][:sys.argv[2].find('.')] + '_compressed.txt')
    elif sys.argv[1] == '-d':
        decompress(sys.argv[2], sys.argv[2][:sys.argv[2].find('_compressed.txt')] + '_decompressed.txt')