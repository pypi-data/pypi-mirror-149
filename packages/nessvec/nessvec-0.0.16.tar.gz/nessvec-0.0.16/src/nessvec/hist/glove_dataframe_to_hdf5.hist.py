"""
# References

* Parquet file format for Dask: https://coiled.io/blog/parquet-file-column-pruning-predicate-pushdown/
* Dask https://pythondata.com/dask-large-csv-python/
* Loaders and academic papers for embeddings: https://github.com/Hironsan/awesome-embedding-models
* Stanford GloVe vectors: https://nlp.stanford.edu/projects/glove/
* 400k 300d GloVe vectors: https://nlp.stanford.edu/data/glove.6B.zip
* FastText 1M 300d vectors loaded here: https://fasttext.cc/docs/en/english-vectors.html
* dataset package simple ORM sql: https://dataset.readthedocs.io/en/latest/
* word2vec c code: https://github.com/dav/word2vec/tree/master/data
* SOTA USE in 2018 was Elmo: https://medium.com/huggingface/universal-word-sentence-embeddings-ce48ddc8fc3a
"""
from pathlib import Path
import pynndescent as pynn
import numpy as np
import h5py
from urllib.request import urlretrieve
import os

import pandas as pd

DATA_DIR = Path('~/nessvec-data').expanduser().resolve().absolute()


STANFORD_GLOVE_PATH = DATA_DIR / 'glove.6B.300d.txt'

chunks = pd.read_csv(
    STANFORD_GLOVE_PATH.open(),
    header=None,
    skiprows=0,
    dtype={0: str},
    index_col=0,
    quoting=3,
    sep=' ',
    chunksize=1000)

# num_vecs = pd.Series([c.shape[0] for c in chunks]).sum()
# num_rows = 300
num_vecs, num_dim = 0, 0
for c in chunks:
    num_vecs, num_dim = c.nrows, c.shape[1]


WIKINEWS_GLOVE_PATH = DATA_DIR / 'wiki-news-300d-1M.vec'
num_vecs, num_dim = WIKINEWS_GLOVE_PATH.open().readline().split()[:2]

chunks = pd.read_csv(
    WIKINEWS_GLOVE_PATH.open(),
    header=None,
    skiprows=1,
    dtype={0: str},
    index_col=0,
    quoting=3,
    sep=' ',
    chunksize=1000)


num_vecs = int(glove_path.open().readline().split()[0])
num_dim = int(glove_path.open().readline().split()[1])
f = h5py.File('/home/hobs/nessvec-data/glove-wiki-news-300d-1M.hdf5', 'a')
dset = f.create_dataset(f'glove{num_vecs}x{num_dim}', (num_vecs, num_dim), dtype=df[1].dtype)

vec = {}
chunks = pd.read_csv(
 or i, chunk in enumerate(chunks):
    rowrange=range(i * 1000, (i + 1) * 1000)
    vec.update(dict(zip(chunk.index.values, rowrange)))
    dset[rowrange, :]=chunk.values

# hist -f 'glove_dataframe_to_hdf5.hist.py'
