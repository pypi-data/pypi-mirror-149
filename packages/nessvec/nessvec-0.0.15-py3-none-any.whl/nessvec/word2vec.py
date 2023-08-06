""" Read binary files containing pretrained word2vec vectors

References:
    - https://github.com/boppreh/word2vec_bin_parser/
    - https://github.com/danielfrg/word2vec
    - https://github.com/Eleanor-H/Argument_Parsing/
    - https://github.com/dkorenci/doc-topic-coherence/tree/master/pytopia/resource/word2vec
"""
import csv
import gzip
from pathlib import Path
import struct
import sys
from tqdm import tqdm

import numpy as np
import pandas as pd


def read_until(stream, sep=b' '):
    while True:
        ch = stream.read(1)
        if ch == sep:
            break
        yield ch  # does not yield the b" " char


def copy_word2vec_bin(infile, outfile=None, limit=1000, num_dim=300):
    """ Copy word2vec bin file to new file (may be limited to top `limit` most frequent words

    Used to create small data files for use in unittests (see `tests/`.
    """
    raise NotImplementedError('Broken implementation')
    inpath = Path(infile)
    indir, infilename = inpath.parent, inpath.name
    if outfile is None:
        outfile = indir / f'{limit}-from-{infilename}'
    if str(outfile).lower().strip().endswith('.bin.gz'):
        opener = gzip.open
    else:
        opener = open
    with opener(outfile, 'wb') as outstream:
        header = f'{limit} {num_dim}\n'.encode()
        print(header)
        outstream.write(header)
        for (i, (word, vec, line)) in enumerate(yield_word_vec_line(infile, limit=limit)):
            if i >= limit:
                break
            print(line)
            outstream.write(line)


def yield_word_vec_lines(filepath: str, limit=np.inf):
    """ Yield word2vec (word, vector) 2-tuples from .bin filepath (pretrained vectors from Google)

    >>> yield_vecs('w2v10000.bin.gz', limit=
    """
    fin = None
    filepath = str(filepath)
    if filepath.endswith('.bin.gz'):
        fin = gzip.open(filepath, 'rb')
    elif filepath.endswith('.bin'):
        fin = open(filepath, 'rb')
    if fin:
        with fin:
            # header=b'3000000 300\n' (num vecs, num_dims)
            header = fin.readline()
            num_vecs, num_dim = map(int, header.split())
            data_struct = 'f' * num_dim
            num_bytes = num_dim * 4
            # while(fin)
            for i in tqdm(range(num_vecs)):
                # lines start with the word itself in utf-8, followed by a space...
                word = b''.join(read_until(fin, sep=b' ')).decode('utf-8')
                vecline = fin.read(num_bytes)
                vector = struct.unpack(data_struct, vecline)
                if i >= limit:
                    break
                yield word, vector, word.encode() + vecline
    else:
        if filepath.endswith('.csv.gz'):
            fin = gzip.open(filepath)
        elif filepath.endswith('.csv.gz'):
            fin = open(filepath, 'rb')
        with fin:
            for (i, (word, vec, line)) in tqdm(enumerate(csv.reader(fin)), total=limit):
                if i >= limit:
                    break
                yield word, vec, line


def yield_vecs(filepath: str, limit=np.inf):
    for word, vector, line in yield_word_vec_lines(filepath=filepath, limit=limit):
        yield word, vector


def read_bin(filepath=None, dest_file=False, num_vecs=None):
    vecs = {}
    csvwriter = None
    if dest_file:
        if dest_file in ('stdout', True):
            csvwriter = csv.writer(sys.stdout)
        elif hasattr(dest_file, 'write'):
            csvwriter = csv.writer(dest_file)
        else:
            csvwriter = csv.writer(open(dest_file, 'wt'))

    for word, vector in yield_vecs(filepath):
        row = [word] + list(vector)
        if csvwriter is not None:
            csvwriter.writerow(row)
        vecs[word] = vector
        if num_vecs is not None and len(vecs) > num_vecs:
            break

    return pd.DataFrame(vecs).T


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('USAGE: python word2vec.py GoogleNews-vectors-negative300.bin.gz')
    else:
        read_bin(filepath=sys.argv[1], dest_file=sys.stdout)
