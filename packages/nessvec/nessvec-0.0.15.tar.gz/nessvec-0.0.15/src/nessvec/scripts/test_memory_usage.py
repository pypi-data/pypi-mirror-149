"""
Use the `memory_profiler` package to measure the memory consumption of the load_hdf5() function

1.2GB on disk and 0GB in RAM for the vectors (80MB for the vocab)

```bash
$ ls -hal ~/nessvec-data/wiki-news-300d-1M.vec.*
-rw-rw-r--  1 hobs hobs 1.2G Jan 15 18:25 wiki-news-300d-1M.vec.hdf5
-rw-rw-r--  1 hobs hobs 511M Jan  8 15:18 wiki-news-300d-1M.vec.parquet

$ python test_memory_usage.py


Filename: /home/hobs/code/tangibleai/nessvec/src/nessvec/test_memory_usage.py

Line #    Mem usage    Increment  Occurrences   Line Contents
=============================================================
    10    109.2 MiB    109.2 MiB           1   @profile
    11                                         def load_hdf5(filepath=str(WIKINEWS_FASTTEXT_PATH) + '.hdf5', encoding='utf8'):
    12    109.9 MiB      0.7 MiB           1       hdf5_file = h5py.File(filepath, 'r')
    13    109.9 MiB      0.0 MiB           1       vecs = hdf5_file['vecs']
    14    109.9 MiB      0.0 MiB           1       vocab = hdf5_file['vocab']
    15    189.7 MiB     79.8 MiB     1999991       vocab = pd.Series(data=range(len(vecs)), index=(s.decode(encoding) for s in vocab))
    16    189.7 MiB      0.0 MiB           1       if len(vocab) != len(vecs):
    17                                                 print(f'vocab len = {len(vocab)} but vecs len = {len(vecs)}')
    18    189.7 MiB      0.0 MiB           1       return vecs, vocab
"""
from constants import DATA_DIR
import h5py
from memory_profiler import profile
import pandas as pd

WIKINEWS_FASTTEXT_PATH = DATA_DIR / 'wiki-news-300d-1M.vec'


@profile
def load_hdf5(filepath=str(WIKINEWS_FASTTEXT_PATH) + '.hdf5', encoding='utf8'):
    hdf5_file = h5py.File(filepath, 'r')
    vecs = hdf5_file['vecs']
    vocab = hdf5_file['vocab']
    vocab = pd.Series(data=range(len(vecs)), index=(s.decode(encoding) for s in vocab))
    if len(vocab) != len(vecs):
        print(f'vocab len = {len(vocab)} but vecs len = {len(vecs)}')
    return vecs, vocab


def main():
    return load_hdf5()


if __name__ == '__main__':
    vecs, vocab = main()
