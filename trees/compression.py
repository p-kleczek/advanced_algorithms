from copy import copy
import itertools
import json
import os
import re
import struct
import settings
from trees.binary_tree import BinaryTreeNode
from utils.paths import make_path

__author__ = 'pawel'

CHARS = 0
FREQ = 1


def count_occurences(encoded_string, chunk_size):
    frequencies = {}

    # Split text into n-chars chunks.
    enc_copy = copy(encoded_string)
    chunks = []
    while len(enc_copy) > chunk_size:
        chunks.append(enc_copy[:chunk_size])
        enc_copy = enc_copy[chunk_size:]
    chunks.append(enc_copy)

    for chunk in chunks:
        if chunk not in frequencies:
            frequencies[chunk] = 0
        frequencies[chunk] += 1
    return frequencies


def construct_huffman_tree(frequencies):
    items = [([ch], freq) for (ch, freq) in frequencies.items()]
    trees = [BinaryTreeNode(item) for item in items]

    # i = 0
    while len(trees) > 1:
        trees = sorted(trees, key=lambda t: t.root_id[1])

        # i += 1
        # print i, [str(t) for t in trees]

        # Wstaw nowe drzewo, w ktorego korzeniu jest suma prawdopodobienstw usunietych drzew,
        # natomiast one same staja sie jego lewym i prawym poddrzewem.
        # Korzen drzewa nie przechowuje symbolu.
        new_chars = trees[0].root_id[CHARS] + trees[1].root_id[CHARS]
        new_freq = trees[0].root_id[FREQ] + trees[1].root_id[FREQ]
        trees.append(BinaryTreeNode((new_chars, new_freq), left=trees[0], right=trees[1]))

        # Usun z listy dwa drzewa o najmniejszym prawdopodobienstwie zapisanym w korzeniu.
        del trees[1]
        del trees[0]

    # print trees[0]
    return trees[0]


def construct_code_page(huffman_tree):
    code_page = {}
    for char in huffman_tree.get_value()[CHARS]:
        code = ''
        node = huffman_tree
        while node.get_value()[CHARS] != [char]:
            if char in node.get_left().get_value()[CHARS]:
                code += '0'
                node = node.get_left()
            else:
                code += '1'
                node = node.get_right()
        code_page[char] = code
    return code_page


def encode(code_page, encoded_string, chunk_size):
    result = ""

    # Split text into n-chars chunks.
    enc_copy = copy(encoded_string)
    chunks = []
    while len(enc_copy) > chunk_size:
        chunks.append(enc_copy[:chunk_size])
        enc_copy = enc_copy[chunk_size:]
    chunks.append(enc_copy)
    num_chunks = len(chunks)

    for chunk in chunks:
        result += code_page[chunk]

    # Split result into chunks of equal length (bytes).
    chunks = []
    CHUNK_BITS = 8
    while len(result) > CHUNK_BITS:
        chunks.append(result[:CHUNK_BITS])
        result = result[CHUNK_BITS:]
    # Fill with zeros.
    chunks.append(result + "0" * (CHUNK_BITS - len(result)))

    return num_chunks, chunks


def store_data(filename_base, code_page, num_chunks, chunks):
    int_chunks = [int(chunk, 2) for chunk in chunks]
    out_file_path = make_path("%s%s_encoded%s" % (settings.OUT_FOLDER, filename_base, settings.HUFFMAN_DATAFILE_EXTENSION))
    with open(out_file_path, "wb") as encoded_file:
        encoded_file.write(struct.pack('I', num_chunks))
        encoded_file.write(bytearray(int_chunks))
    out_file_path = make_path("%s%s_encoding%s" % (settings.OUT_FOLDER, filename_base, settings.HUFFMAN_DATAFILE_EXTENSION))
    json.dump(code_page, open(out_file_path, 'w'))


def load_data(filename_base):
    in_file_path = make_path("%s%s_encoding%s" % (settings.OUT_FOLDER, filename_base, settings.HUFFMAN_DATAFILE_EXTENSION))
    code_page = json.load(open(in_file_path))
    in_file_path = make_path("%s%s_encoded%s" % (settings.OUT_FOLDER, filename_base, settings.HUFFMAN_DATAFILE_EXTENSION))
    file_size = os.path.getsize(in_file_path)
    with open(in_file_path, "rb") as encoded_file:
        (num_chars,) = struct.unpack('I', encoded_file.read(4))
        n_bytes = file_size-4
        bytes = list(struct.unpack('%dB' % n_bytes, encoded_file.read(n_bytes)))
    to_bin = lambda i: format(i, '08b')
    encoded_string = ''.join(map(to_bin, bytes))

    # print encoded_string

    return code_page, num_chars, encoded_string


def decode(code_page, num_chars, encoded_string):
    # Swap keys and values
    reverse_code_page = dict(zip(code_page.values(), code_page.keys()))
    max_key_length = max([len(k) for k in reverse_code_page.keys()])

    result = ""
    start = stop = 0
    if not settings.SURPRESS_OUTPUT:
        print "Number of chunks to decode:", num_chars
    total_iterations = num_chars
    iterations_per_one_percent = num_chars / 100
    for i in xrange(num_chars):
        while encoded_string[start:stop] not in reverse_code_page:
            stop += 1
            if stop - start > max_key_length:
                data = {
                    'chunk_id': i +1,
                }
                print result
                raise Exception("Exceeded max key length! (Chunk #%(chunk_id)d)" % data)
        result += reverse_code_page[encoded_string[start:stop]]
        start = stop

        if not settings.SURPRESS_OUTPUT:
            if iterations_per_one_percent == 0:
                print "[HUFFMAN] %d%% finished" % (i * 100 / total_iterations)
            elif i % iterations_per_one_percent == 0 and i > 0:
                print "[HUFFMAN] %d%% finished" % (i / iterations_per_one_percent)

    return result


def huffman(filename_base, chunk_size):
    encoded_string = ""
    in_file_path = make_path("%s%s%s" % (settings.DATA_FOLDER, filename_base, settings.HUFFMAN_DATAFILE_EXTENSION))
    with open(in_file_path) as f:
        for line in f:
            encoded_string += unicode(line, errors='replace') + u'\n'

    if settings.DEBUG:
        encoded_string = u"TO BE OR\n NOT TO BE"
    frequencies = count_occurences(encoded_string, chunk_size)
    tree = construct_huffman_tree(frequencies)
    code_page = construct_code_page(tree)
    if not settings.SURPRESS_OUTPUT:
        print code_page

    num_chunks, chunks = encode(code_page, encoded_string, chunk_size)

    store_data(filename_base, code_page, num_chunks, chunks)
    code_page, num_chars, encoded_string = load_data(filename_base)
    decoded_string = decode(code_page, num_chars, encoded_string)

    if not settings.SURPRESS_OUTPUT:
        print ">> decoded string:", decoded_string

    out_file_path = make_path("%s%s_decoded%s" % (settings.OUT_FOLDER, filename_base, settings.HUFFMAN_DATAFILE_EXTENSION))
    with open(out_file_path, 'w') as f:
        f.write(decoded_string.encode('utf8'))