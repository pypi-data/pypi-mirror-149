""" File Management module

# Data sources

# Pre-trained FASTTEXT word vectors:

1. [wiki-news-300d-1M.vec.zip](https://dl.fbaipublicfiles.com/fasttext/vectors-english/wiki-news-300d-1M.vec.zip):
  - 1M word vectors
  - Wikipedia 2017, UMBC webbase corpus and statmt.org news dataset (16B tokens)
2. [wiki-news-300d-1M-subword.vec.zip](https://dl.fbaipublicfiles.com/fasttext/vectors-english/wiki-news-300d-1M-subword.vec.zip):
  - 1M word vectors
  - trained on subwords from Wikipedia 2017 subwords, UMBC webbase corpus, and statmt.org news (16B tokens).
3. [crawl-300d-2M.vec.zip](https://dl.fbaipublicfiles.com/fasttext/vectors-english/crawl-300d-2M.vec.zip):
  - 2M word vectors
  - Common Crawl (600B tokens)
4. [crawl-300d-2M-subword.zip](https://dl.fbaipublicfiles.com/fasttext/vectors-english/crawl-300d-2M-subword.zip)
  - 2M word vectors
  - subwords from Common Crawl (600B tokens)
"""
# from __future__ import absolute_import
import csv
# from csv import QUOTE_MINIMAL     # 0 # noqa
# from csv import QUOTE_ALL         # 1 # noqa
# from csv import QUOTE_NONNUMERIC  # 2 # noqa
# from csv import QUOTE_NONE        # 3 # noqa
import logging
from pathlib import Path
import re
import requests
from urllib.request import urlretrieve
from zipfile import ZipFile

import h5py
import numpy as np
import pandas as pd
from tqdm import tqdm

from .constants import DATA_DIR
from .word2vec import copy_word2vec_bin

# from . import word2vec

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


DEFAULT_EMBEDDING_ALGORITHM = 'fasttext'


# https://github.com/mmihaltz/word2vec-GoogleNews-vectors
DEFAULT_RAW_WORD2VEC_FILENAME = 'GoogleNews-vectors-negative300.bin.gz'

###########################################################################
# GloVE

# https://nlp.stanford.edu/projects/glove/
GLOVE_BASE_URL = 'https://nlp.stanford.edu/data'
DEFAULT_RAW_GLOVE_FILENAME = 'glove.6B.300d.txt'
DEFAULT_VEC_GLOVE_FILENAME = 'glove.6B.300d.txt'
# mirrored to DropBox to facilitate programmatic download without git lfs
DEFAULT_RAW_GLOVE_URL = GLOVE_BASE_URL + '/' + DEFAULT_RAW_GLOVE_FILENAME
DEFAULT_RAW_GLOVE_PATH = DATA_DIR / DEFAULT_RAW_GLOVE_FILENAME
DEFAULT_HDF5_GLOVE_FILENAME = DEFAULT_RAW_GLOVE_FILENAME[:-4] + '.hdf5'
DEFAULT_HDF5_GLOVE_PATH = DATA_DIR / DEFAULT_HDF5_GLOVE_FILENAME

# GloVE
###########################################################################

############################################################################
# FastText
#
# https://fasttext.cc/docs/en/english-vectors.html
DEFAULT_RAW_FASTTEXT_FILENAME = 'wiki-news-300d-1M.vec.zip'
DEFAULT_VEC_FASTTEXT_FILENAME = 'wiki-news-300d-1M.vec'
# https://fasttext.cc/docs/en/pretrained-vectors.html
FASTTEXT_BASE_URL = 'https://dl.fbaipublicfiles.com/fasttext/vectors-english'
FASTTEXT_URLS = [
    '/'.join([FASTTEXT_BASE_URL, 'wiki-news-300d-1M.vec.zip']),
    '/'.join([FASTTEXT_BASE_URL, 'wiki-news-300d-1M-subword.vec.zip']),
    '/'.join([FASTTEXT_BASE_URL, 'crawl-300d-2M.vec.zip']),
    '/'.join([FASTTEXT_BASE_URL, 'crawl-300d-2M-subword.zip']),
]
DEFAULT_RAW_FASTTEXT_URL = FASTTEXT_BASE_URL + '/' + DEFAULT_RAW_FASTTEXT_FILENAME
DEFAULT_RAW_FASTTEXT_PATH = DATA_DIR / DEFAULT_RAW_FASTTEXT_FILENAME

#
# FastText
############################################################################


############################################################################
# word2vec
#
# FIXME: WORD2VEC_BASE_URL = 'https://proai.org'

WORD2VEC_BASE_URL = 'https://www.dropbox.com/sh/5lt3jy6n58vtw2c/AADR2Yh5bbzaKNiBabMuuRgVa'
DEFAULT_RAW_WORD2VEC_FILENAME = 'GoogleNews-vectors-negative300.bin.gz'
DEFAULT_VEC_WORD2VEC_FILENAME = DEFAULT_RAW_WORD2VEC_FILENAME
DEFAULT_RAW_WORD2VEC_URL = WORD2VEC_BASE_URL + '/' + DEFAULT_RAW_WORD2VEC_FILENAME
DEFAULT_RAW_WORD2VEC_PATH = DATA_DIR / DEFAULT_RAW_WORD2VEC_FILENAME
WORD2VEC_URLS = [
    'https://www.dropbox.com/sh/5lt3jy6n58vtw2c/AADR2Yh5bbzaKNiBabMuuRgVa/GoogleNews-vectors-negative300.bin.gz?dl=1',
]
DEFAULT_HDF5_WORD2VEC_FILENAME = DEFAULT_RAW_WORD2VEC_FILENAME[:-7] + '.hdf5'
DEFAULT_HDF5_WORD2VEC_PATH = DATA_DIR / DEFAULT_HDF5_WORD2VEC_FILENAME


# word2vec
############################################################################

DEFAULT_HDF5_FILENAMES = pd.Series(dict(
    fasttext='fasttext-wiki-news-300d-1M.hdf5',
    glove='glove.6B.300d.hdf5',
    word2vec='word2vec-GoogleNews-vectors-negative300.hdf5',
))


# see: https://fasttext.cc/docs/en/english-vectors.html
EMBEDDING_ALGORITHM_SIZE_FILENAMES = pd.DataFrame([
    [
        'fasttext', 'wiki', 'news', 'small', 'word',
        'wiki-news-300d-1M.vec.zip',
        "1 million word vectors trained on Wikipedia 2017, UMBC webbase corpus and statmt.org news dataset (16B tokens)",
    ],
    [
        'fasttext', 'wiki', 'news', 'large', 'subword',
        'wiki-news-300d-1M-subword.vec.zip',
        "",
    ],
    [
        'glove',
        'glove.6B.300d.hdf5',
        "",
    ],
    [
        'word2vec',
        'word2vec-GoogleNews-vectors-negative300.hdf5',
        "",
    ],
])


DEFAULT_RAW_FILENAMES = pd.Series(dict(
    fasttext=DEFAULT_RAW_FASTTEXT_FILENAME,
    glove=DEFAULT_RAW_GLOVE_FILENAME,
    word2vec=DEFAULT_RAW_WORD2VEC_FILENAME,
))

DEFAULT_RAW_URLS = pd.Series(dict(
    fasttext=DEFAULT_RAW_FASTTEXT_URL,
    glove=DEFAULT_RAW_GLOVE_URL,
    word2vec=DEFAULT_RAW_WORD2VEC_URL
))


DEFAULT_VEC_FILENAMES = pd.Series(dict(
    fasttext=DEFAULT_VEC_FASTTEXT_FILENAME,
    glove=DEFAULT_VEC_GLOVE_FILENAME,
    word2vec=DEFAULT_VEC_WORD2VEC_FILENAME,
))


# https://fasttext.cc/docs/en/pretrained-vectors.html
FASTTEXT_URLS = [
    'https://dl.fbaipublicfiles.com/fasttext/vectors-english/wiki-news-300d-1M.vec.zip',
    'https://dl.fbaipublicfiles.com/fasttext/vectors-english/wiki-news-300d-1M-subword.vec.zip',
    'https://dl.fbaipublicfiles.com/fasttext/vectors-english/crawl-300d-2M.vec.zip',
    'https://dl.fbaipublicfiles.com/fasttext/vectors-english/crawl-300d-2M-subword.zip',
]

WORD2VEC_URLS = [
    'https://www.dropbox.com/sh/5lt3jy6n58vtw2c/AADR2Yh5bbzaKNiBabMuuRgVa/GoogleNews-vectors-negative300.bin.gz?dl=1',
]


def stanford_words(url='https://nlp.stanford.edu/~lmthang/morphoNLM/cwCsmRNN.words'):
    filepath = download(url, filepath='morphoNLM.words')
    return open(filepath).readlines()


def load_stanford_morpho_em(
        url='http://www-nlp.stanford.edu/~lmthang/morphoNLM/rw.zip',
        filenames=['rw/rw.txt']):
    """ Download dataset for the Stanford RNN Morphology Language Model for word embeddings

    Returns a DataFrame with word pairs scored for similarity and 9-D manual embeddings?

    >>> stanford_morpho_embedding()
                      0              1     2   3   4   ...  8   9    10   11    12
    0         squishing         squirt  5.88   7   7  ...   6   6   7.0  2.0   4.0
    1           undated      undatable  5.83  10   9  ...   7   7   9.0  2.0   5.0
    2       circumvents           beat  5.33   7   7  ...   6   3   2.0  0.0   6.0
    3       circumvents            ebb  3.25   7   4  ...   0   0   3.0  6.0   0.0

    """
    filepath = download(url)
    filepaths = unzip_files(filepath, filenames=filenames)
    return pd.read_csv(filepaths[0], sep='\t', header=None)


"""
  title: "Better Word Representations with Recursive Neural Networks for Morphology"
  url: http://www-nlp.stanford.edu/~lmthang/morphoNLM/rw.zip
  urls:
    - "https://nlp.stanford.edu/~lmthang/morphoNLM/cwCsmRNN.words"
    - "https://nlp.stanford.edu/~lmthang/morphoNLM/"
  description: |+
    [Better Word Representations with Recursive Neural Networks for Morphology](https://nlp.stanford.edu/~lmthang/morphoNLM/)
    # `rw/rw.txt` (92.5 kB, 2034 lines):
    ```text
    squishing squirt  5.88  7 7 6 1 4 6 6 7 2 4
    undated undatable 5.83  10  9 6 5 5 7 7 9 2 5
    circumvents beat  5.33  7 7 3 9 8 6 3 2 0 6
    circumvents ebb 3.25  7 4 6 4 2 0 0 3 6 0
    ```
    # `rw/rw.txt` (92.5 kB):
    ```text
    >>> words = open('cwCsmRNN.words').readlines()
    >>> len(words)
    138218
    >>> words[1000:1005]
    ['0kb', '0kbushel', '0keystart', '0kg', '0-kg']
    ```
"""


def reporthook(block_num, read_size, total_size):
    r""" tqdm wrapper to comply with urllib.request.urlretrieve() reporthook kwarg

    TODO: turn this into a class that inherits tqdm and can be used within a context manager

    From urllib.request.urlretrieve:
      "The reporthook argument should be a callable that accepts
       a block number, a read size, and the total file size of the URL target."
    """
    # log.debug(f'\nblock_num={block_num}\n  read_size={read_size}\n  total_size={total_size}')
    if reporthook.pbar is None or block_num < 1:
        reporthook.downloaded = 0
        reporthook.pbar = tqdm(total=total_size)
    reporthook.downloaded += read_size
    # log.debug(f'  downloaded={downloaded}\n')
    if reporthook.downloaded < total_size:
        reporthook.pbar.update(read_size)
    else:
        reporthook.pbar.close()
        reporthook.pbar = None


reporthook.downloaded = 0
reporthook.pbar = None


class VecDialect(csv.Dialect):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        super().__init__()


def load_vecs_df(filepath=DEFAULT_RAW_GLOVE_PATH, skiprows=1, **kwargs):
    """ Load Stanford GloVe vectors from .txt file into pandas.DataFrame

    Detects and ignores possible header line containing 2 ints: num_rows num_cols
    GloVE does not contain a header, but FastText and Word2Vec do.

    skiprows (int, list): int: number of rows, list: row indices (0-offset) to skip
    header (int, None): int: num rows to use for column labels

    TODO: use chunksize to create and load hdf5 file on the fly.
    """
    log.debug(f"skiprows={skiprows}")
    if skiprows is None:
        try:
            shape = [int(s) for s in open(filepath).readline().split()]
            if len(shape) == 2:
                skiprows = 1
        except (TypeError, ValueError):
            log.warning("No header found. Using skiprows={skiprows}")
            skiprows = None
    # dtype = dict(zip(range(4099), [str] + [float]*4098))
    df = pd.read_csv(
        filepath,
        index_col=0,
        header=None,
        skiprows=1,
        dtype={0: str},
        quoting=3,
        sep=' ',
        **kwargs
    )
    df.columns = range(len(df.columns))
    return df
    # return pd.read_csv(
    #     str(filepath),
    #     index_col=index_col,
    #     header=header,
    #     skiprows=skiprows,
    #     dtype=dtype,
    #     quoting=quoting,
    #     sep=sep,
    #     encoding=encoding)


# size: 6B | 42B | 84B | twitter.27B
GLOVE_ZIP_FILENAME_TEMPLATE = 'glove.{size}B.zip'
GLOVE_URL_TEMPLATE = 'https://nlp.stanford.edu/data/' + GLOVE_ZIP_FILENAME_TEMPLATE

# dim: 50 | 100 | 300 | 1000
GLOVE_FILENAME_TEMPLATE = 'glove.{size}B.{dim}d.txt'

# https://nlp.stanford.edu/projects/glove/
STANFORD_GLOVE_URLS = pd.Series({
    6: 'https://nlp.stanford.edu/data/glove.6B.zip',
    27: 'https://nlp.stanford.edu/data/glove.twitter.27B.zip',
    42: 'https://nlp.stanford.edu/data/glove.42B.300d.zip',
    840: 'https://nlp.stanford.edu/data/glove.840B.300d.zip',
})


def load_large_glove_df(dim=50, size=6):
    """ Download and return the specified GloVe word vectors DataFrame from Stanford

    Inputs:
        size (int): 6B | 42B | 84B | twitter.27B (default=6)
        dim (int): 50 | 100 | 300 | 1000 (default=50)

    >>> wv = load_glove_df(dim=50, size=42)
    >>> wv.shape
    (400000, 300)
    >>> wv = load_glove_df(dim=50, size=6)
    >>> wv.shape
    (400000, 50)
    """
    size = str(size).lower().rstrip('b')
    try:
        filepath = download_glove_if_necessary(size)
    except Exception as e:
        log.warning(f"Unable to download_glove with size={size}")
        raise(e)
    if int(size) > 6:
        log.warning(f'Size {size} does not have dim={dim}')
        dim = 300
    dim = str(dim).lower().rstrip('d')
    filepath = Path(DATA_DIR).joinpath(
        GLOVE_FILENAME_TEMPLATE.format(dim=dim, size=size))
    zippath = Path(filepath).parent.joinpath(GLOVE_ZIP_FILENAME_TEMPLATE.format(size=size))
    filepath = unzip_glove(zippath)
    return load_vecs_df(filepath)


def make_path_obj(path):
    if isinstance(path, str):
        path = Path(path)
    return path.expanduser().resolve().absolute()


resolve_path = make_path_obj


def unzip_files(zip_filepath, filename=None, filenames=None, data_dir=DATA_DIR):
    r""" Decompress .zip format into the same directory as zip_filepath

    >>> zip_filepath = download('http://www-nlp.stanford.edu/~lmthang/morphoNLM/rw.zip')
    >>> unzip_files(zip_filepath)
    """
    if isinstance(filename, str) and filename.lower().strip() not in ('all', '*', ''):
        filenames = [filename]
    zip_filepath = make_path_obj(zip_filepath)
    with ZipFile(str(zip_filepath), 'r') as zipobj:
        if filenames is None:
            filenames = zipobj.namelist()
        for fn in filenames:
            zipobj.extract(str(fn), path=data_dir)
    dest_filepaths = [data_dir.joinpath(fn) for fn in filenames]
    return dest_filepaths


def unzip_glove(zip_filepath, filename=None, dim=None, size=None):
    """ Extract txt files from ZipFile and place them all in the dest_filepath or DATA_DIR """
    zip_filepath = Path(zip_filepath)
    sizematch = re.search(r'[.](\d{1,3})B[.]', str(zip_filepath))
    if sizematch:
        size = int(sizematch.groups()[0])
    if filename is None and (dim or size):
        filename = GLOVE_FILENAME_TEMPLATE.format(dim=(dim or 50), size=(size or 6))
    dest_filepaths = unzip_files(zip_filepath, filename=filename)

    return dest_filepaths


def guess_filepath(url=None, filename=None, filepath=None, data_dir=DATA_DIR):
    data_dir = make_path_obj(data_dir)
    if not data_dir.is_dir():
        data_dir.mkdir()
    log.warning(f"data_dir='{data_dir}'")

    if not filepath:
        if not filename:
            if not url:
                raise ValueError("You must specify at least one of `filename`, `filepath`, or `url`.")
            filename = str(url).split('/')[-1]
            filename = filename.split('?')[0]
        filepath = data_dir / filename
    return make_path_obj(filepath)


def download_with_requests(url, data_dir=DATA_DIR, filepath=None, filename=None):
    filepath = guess_filepath(url=url, filename=filename, filepath=filepath, data_dir=data_dir)

    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko)"
    headers = {'User-Agent': user_agent}

    # using requests to download and open file
    with requests.get(url, stream=True, headers=headers) as resp:
        with filepath.open('wb') as fout:
            for chunk in tqdm(resp.iter_content(chunk_size=8192)):
                fout.write(chunk)

    return filepath


def download(url, data_dir=DATA_DIR, filepath=None, filename=None, reporthook=reporthook):
    """ Download a file from a url and put it in data_dir or filepath or DATA_DIR/filename

    >> download('https://nlp.stanford.edu/data/glove.6B.zip')
    .nlpia2-data/glove.6B.zip'
    """
    log.warning(f"starting download(url='{url}', filepath='{filepath}')")
    filepath = guess_filepath(url=url, filename=filename, filepath=filepath, data_dir=data_dir)
    log.warning(f"guess_filepath() returned: '{filepath}'")

    if not filepath.is_file():
        # FIXME: reporthook seems broken
        try:
            urlretrieve(url, filepath, reporthook=reporthook)
        except Exception as e:
            log.warning(f"Unable to download_url='{url}'")
            raise(e)

    return filepath


# def load_ann_benchmark(name='glove-100-anglular'):
#     url = f"http://ann-benchmarks.com/{name}.hdf5"
#     filepath = DATA_DIR / f"{name}.hdf5"
#     if not filepath.is_file():
#         log.debug(f"Dataset {name} is not cached; downloading now ...")
#         urlretrieve(url, filepath, show_progress)
#     return h5py.File(filepath, "r")
    # return np.array(hdf5_file['train']), np.array(hdf5_file['test']), hdf5_file.attrs['distance']


def load_ann_benchmark(name='glove-100-angular'):
    url = f"http://ann-benchmarks.com/{name}.hdf5"
    filepath = DATA_DIR / f"{name}.hdf5"
    if not filepath.is_file():
        log.warning(f"Dataset {name} is not yet cached; downloading now ...")
        urlretrieve(url, filepath, reporthook=reporthook)
    return h5py.File(filepath, "r")


# FIXME: RAW_PATH ('/home/hobs/.nlpia2-data/wiki-news-300d-1M.vec.zip') is zip file
#        it needs to be unzipped before this will work
#        and dest hdf5 path needs to be different than unzipped path
# FIXME: make it work for word2vec .bin files using word2vec.yield_vecs
def vecs_to_hdf5(filepath=DEFAULT_RAW_FASTTEXT_PATH,
                 skiprows=1, quoting=csv.QUOTE_NONE, sep=' ',
                 encoding='utf8',
                 header=None, chunksize=10000, **kwargs):
    """ Convert FASTTEXT .vec file into chunked hdf5 file format for out-of-core processing

    For fasttext and word2vec skiprows=1 to avoid header containing shape of dataframe
    References:
        Efficient hdf5 file creation using chunking of pd.read_csv(): https://stackoverflow.com/a/34533601/623735
    """
    num_vecs, num_dims = None, None
    try:
        num_vecs, num_dims = [int(i) for i in Path(filepath).open().readline().split()]
    except (ValueError, TypeError):
        log.warning("Filepath '{filepath}' doesn't appear to contain a fasttext-formatted header line with df.shape.")

    if num_vecs:
        log.info(f"Loading {num_vecs}x{num_dims} word vectors from '{filepath}'.")
        # vocab is read into RAM in its entirety to avoid truncation of the longer strings if read in chunks
        vocab = pd.read_csv(
            filepath,
            header=header,
            skiprows=skiprows,
            dtype={0: str},
            usecols=[0],
            quoting=quoting,
            sep=sep,
        )[0]
        vocab = vocab.str.encode('utf8').astype(bytes)
        vec_chunks = pd.read_csv(
            str(filepath),
            skiprows=skiprows,
            quoting=quoting,
            sep=sep,
            header=header,
            dtype=np.float32,
            usecols=range(1, num_dims + 1),
            # encoding='latin',
            chunksize=chunksize,
            **kwargs)

    filepath_hdf5 = str(filepath) + '.hdf5'

    with h5py.File(filepath_hdf5, 'w') as f:
        # Initialize a resizable dataset to hold the output
        dset_vecs = f.create_dataset(
            'vecs',
            shape=(num_vecs, num_dims),
            chunks=(chunksize, num_dims),
            dtype=np.float32)
        dset_vocab = f.create_dataset('vocab', data=vocab)  # noqa

        rownum = 0
        for vec_chunk in vec_chunks:
            dset_vecs[rownum:rownum + vec_chunk.shape[0]] = vec_chunk
            rownum += vec_chunk.shape[0]

    return filepath_hdf5


def download_word2vec(url=None):
    """ Download the Google News word2vec pretrained word vectors """
    if url is None:
        url = WORD2VEC_URLS[0]
    return download(url=url)


def download_word2vec_if_necessary(url=None):
    """ Download the Google News word2vec pretrained word vectors """
    if url is None:
        url = WORD2VEC_URLS[0]
    algorithm, filepath = guess_algorithm_filepath(url=url)
    filepath = make_path_obj(filepath)
    if filepath.is_file():
        return filepath
    log.warning(f"Can't find {filepath} so downloading from '{url}'.")
    return download(url=url)


def download_glove_if_necessary(size=6, url=None, dest_filepath=None):
    """ download and extract text file containig pairs of translated phrases

    Inputs:
        corpus (str): 6B | 42B | 84B | twitter.27B
        url (full url to the zip file containing a GloVe vector model)
    Returns:
        path_to_zipfile (str)
    """
    url = url or guess_glove_url(size=size)
    algorithm, filepath = guess_algorithm_filepath(url=url)
    filepath = make_path_obj(filepath)
    if algorithm != 'glove':
        log.warning(
            f"URL '{url}' from size '{size}' doesn't appear to contain a GloVE filename (filename found: '{filepath}').")
    if not filepath.is_file():
        log.warning(f"Can't find '{filepath}'")
        filepath = download_glove(size)
    return filepath


def guess_glove_url(size=6):
    size = str(size).lower().strip()
    size = size.rstrip('b')
    return STANFORD_GLOVE_URLS[int(size)]


def download_glove(size=6, url=None, dest_filepath=None):
    """ download and extract text file containig pairs of translated phrases

    Inputs:
        corpus (str): 6B | 42B | 84B | twitter.27B
        url (full url to the zip file containing a GloVe vector model)
    Returns:
        path_to_zipfile (str)
    """
    url = url or guess_glove_url(size=size)
    # if size.endswith('27'):
    #     size = 'twitter.27'
    # url = url or GLOVE_URL_TEMPLATE.format(size=size)
    log.warning(url)
    return download(url=url)


def download_fasttext_hdf5(num_million_vecs=1, subwords=False, url=None, dest_filepath=None):
    """ download and extract text file containig pairs of translated phrases

    FASTTEXT_URLS = [
        'https://dl.fbaipublicfiles.com/fasttext/vectors-english/wiki-news-300d-1M.vec.zip',
        'https://dl.fbaipublicfiles.com/fasttext/vectors-english/crawl-300d-2M.vec.zip',
        'https://dl.fbaipublicfiles.com/fasttext/vectors-english/wiki-news-300d-1M-subword.vec.zip',
        'https://dl.fbaipublicfiles.com/fasttext/vectors-english/crawl-300d-2M-subword.zip',
    ]
    Returns:
        path_to_zipfile (str)
    """
    base_url = FASTTEXT_BASE_URL  # https://dl.fbaipublicfiles.com/fasttext/vectors-english
    filenames = [
        'wiki-news-300d-1M.vec.zip',
        'crawl-300d-2M.vec.zip',
        'wiki-news-300d-1M-subword.vec.zip',
        'crawl-300d-2M-subword.zip',
    ]
    subwords = int(subwords)
    num_million_vecs = int(num_million_vecs)

    filename = filenames[subwords * 2 + num_million_vecs - 1]

    if url is None:
        url = base_url + '/' + filename
    try:
        log.info(f'Downloading {url} to {filename}...')
        zip_filepath = download(url=url, filename=filename)
    except Exception as e:
        log.error(f'Unable to `download(url={url}, filename={filename})`')
        raise e
    log.info(f'Unzipping {zip_filepath}...')
    filepaths = unzip_files(zip_filepath)
    hdf5_filepaths = []
    for fp in filepaths:
        if str(fp).lower().startswith('readme'):
            continue
        log.info(f'Converting {fp} to hdf5...')
        hdf5_fp = vecs_to_hdf5(filepath=fp)
        hdf5_filepaths.append(hdf5_fp)
    if len(hdf5_filepaths) > 1:
        return hdf5_filepaths
    return hdf5_filepaths[0]


def load_fasttext_hdf5(filepath=str(DEFAULT_RAW_FASTTEXT_PATH) + '.hdf5', encoding='utf8', num_vecs=None):
    filepath = str(filepath)
    hdf5_file = h5py.File(filepath, 'r')
    vecs = hdf5_file['vecs'][:num_vecs]  # TODO FIXME: may not work if None is used in slicer
    vocab = hdf5_file['vocab'][:num_vecs]
    vocab = pd.Series(data=range(len(vecs)), index=(s.decode(encoding) for s in vocab))
    if len(vocab) != len(vecs):
        log.error(f'vocab len = {len(vocab)} but vecs len = {len(vecs)}')
    return vecs, vocab


def load_hdf5_df(filepath, encoding='utf8', num_rows=None):
    data, idx = load_hdf5_data_index(filepath, encoding=encoding, num_rows=num_rows)
    df = pd.DataFrame(data, index=idx.index.values)
    return df


def load_hdf5_data_index(filepath, encoding='utf8', num_rows=None):
    filepath = str(filepath)
    hdf5_file = h5py.File(filepath, 'r')

    # TODO using NLP to identify data/vecs and index/vocab within hdf5_file.keys()
    try:
        data = hdf5_file['vecs'][:num_rows]  # TODO FIXME: may not work if None is used in slicer
    except KeyError:
        data = hdf5_file['data'][:num_rows]

    try:
        idx = hdf5_file['vocab'][:num_rows]
    except KeyError:
        idx = hdf5_file['index'][:num_rows]

    idx = pd.Series(data=range(len(idx)), index=(s.decode(encoding) for s in idx))
    if len(idx) != len(data):
        log.error(f'index len = {len(idx)} but data len = {len(data)}')
    return data, idx


def load_glove_hdf5(filepath=DEFAULT_HDF5_GLOVE_PATH, **kwargs):
    return load_fasttext_hdf5(filepath, **kwargs)


def load_word2vec_hdf5(filepath=DATA_DIR / DEFAULT_HDF5_WORD2VEC_FILENAME, **kwargs):
    return load_hdf5_df(filepath, **kwargs)


def guess_algorithm_filepath(filepath=DEFAULT_EMBEDDING_ALGORITHM, **kwargs):
    """ Guess the filepath and kind of word embeddings (algorithm) the user wants to load.

    >>> guess_algorithm_filepath('glove')
    ('glove', '...glove.6B.300d.hdf5')
    """
    algorithm = kwargs.pop('algorithm', 'fasttext')
    for algo in DEFAULT_RAW_FILENAMES:
        if algo in filepath.lower():  # FIXME: fails on word2vec because named GoogleNews...
            algorithm = algo
            break
    if not Path(filepath).is_file():
        filename = DEFAULT_RAW_FILENAMES[algorithm]
        filepath = DATA_DIR / filename
    return algorithm, filepath


def csv_to_hdf5(filepath, name='data', chunksize=10000, dtype=None, **kwargs):
    """ Use pd.read_csv(chunksize=...) when converting CSV to hdf5 (low memory)

    FIXME: merge code with `def df_to_hdf5()`
    TODO: use this to convert csv file containing strs for wikipedia titles to hdf5
    SEE: df_to_hdf5()

    >>> filepath = "wikipedia-20220228-titles-all-in-ns0.csv.gz"
    >>> csv_to_hdf5(filepath, dtype=np.dtype(str))
    ValueError: Size must be positive (size must be positive)
    """
    # if isinstance(data, (pd.Series, np.ndarray, list, tuple)):
    #     df = pd.DataFrame()
    #     df['0'] = data
    # elif not isinstance(data, pd.DataFrame):
    chunks = pd.read_csv(filepath, chunksize=chunksize, header=0, **kwargs)
    num_rows = 0
    num_cols = 0
    data_dtype = dtype or None
    index_dtype = None
    for chunk in chunks:
        num_rows += len(chunk)
        num_cols = max(num_cols, chunk.shape[1])
        data_dtype = data_dtype or chunk.values.dtype
        index_dtype = index_dtype or chunk.index.values.dtype

    if data_dtype in (np.dtype("O"), np.dtype(str)):
        data_dtype = np.dtype(bytes)

    filepath_hdf5 = str(filepath) + '.hdf5'

    log.debug(f"data_: dtype={data_dtype}\nshape={(num_rows, num_cols)}\nchunkshape={(chunksize, num_cols)}")
    log.debug(f"index_: dtype={index_dtype}\nshape={(num_rows,)}\nchunkshape={(chunksize,)}")

    with h5py.File(filepath_hdf5, 'w') as f:
        # Initialize a resizable dataset to hold the output
        dset_data = f.create_dataset(
            name,
            shape=(num_rows, num_cols),
            chunks=(chunksize, num_cols),
            dtype=data_dtype)
        dset_index = f.create_dataset(
            'index',
            shape=(num_rows,),
            chunks=(chunksize,),
            dtype=index_dtype)

        chunks = pd.read_csv(filepath, chunksize=chunksize, **kwargs)

        rownum_end = 0
        for chunk in chunks:
            rownum_start = rownum_end
            rownum_end += chunk.shape[0]
            dset_data[rownum_start:rownum_end] = chunk.str.encode()
            dset_index[rownum_start:rownum_end] = chunk.index
    return filepath_hdf5


def df_to_hdf5(df, filepath='df.hdf5', name='data', chunksize=10000, dtype=None, **kwargs):
    """ Write dataframe to hdf4 with index in array 'index' and data/values in array 'data'

    FIXME: make this work with chunked DataFrames: df=pd.read_csv(filepath, chunksize=...)
    SEE: csv_to_hdf5()

    >>> filepath = "wikipedia-20220228-titles-all-in-ns0.csv.gz"
    >>> csv_to_hdf5(filepath, dtype=np.dtype(str))
    ValueError: Size must be positive (size must be positive)
    """
    # if isinstance(data, (pd.Series, np.ndarray, list, tuple)):
    #     df = pd.DataFrame()
    #     df['0'] = data
    # elif not isinstance(data, pd.DataFrame):

    num_rows, num_cols = df.shape
    data = df.values
    if data.dtype in (np.dtype("O"), np.dtype(str)):
        data = data.astype('S')
    idx = df.index.values
    if idx.dtype in (np.dtype("O"), np.dtype('str'), np.dtype('bytes')):
        idx = df.index
        if not isinstance(idx.values[0], bytes):
            idx = idx.str.encode('utf-8')
        idx = idx.values.astype('S')

    log.debug(f"data_: dtype={data.dtype}\nshape={(num_rows, num_cols)}\nchunkshape={(chunksize, num_cols)}")
    log.debug(f"index_: dtype={idx.dtype}\nshape={(num_rows,)}\nchunkshape={(chunksize,)}")

    filepath_hdf5 = str(filepath)

    with h5py.File(filepath_hdf5, 'w') as f:
        # Initialize a resizable dataset to hold the output
        chunks = [d for d in data.shape]
        chunks[0] = chunksize
        dset_data = f.create_dataset(
            name,
            shape=data.shape,
            chunks=tuple(chunks),
            dtype=data.dtype)

        chunks = [d for d in idx.shape]
        chunks[0] = chunksize
        dset_index = f.create_dataset(
            'index',
            shape=idx.shape,
            chunks=tuple(chunks),
            dtype=idx.dtype)
        dset_data[:] = data
        dset_index[:] = idx
    return filepath_hdf5


def create_word2vec_testfiles(algorithms=(('word2vec', copy_word2vec_bin),), limit=1000):
    for algo, copyfun in algorithms:
        copyfun(
            infile=DATA_DIR / DEFAULT_RAW_FILENAMES[algo],
            outfile=DATA_DIR / f'{algo}-{limit}.bin',
            limit=limit)


def load_fasttext_df(num_vecs=None, algoname='fasttext'):
    """ Load a word embeddings from a fasttext hdf5 file and memory-map to a DataFrame """
    hdf5filepath = DATA_DIR / Path(DEFAULT_HDF5_FILENAMES[algoname])
    if not hdf5filepath.is_file():
        log.debug(f"No hdf5 file found at '{str(hdf5filepath)}'")
        vecfilepath = DATA_DIR / Path(DEFAULT_VEC_FILENAMES[algoname])
        rawfilepath = DATA_DIR / Path(DEFAULT_RAW_FILENAMES[algoname])
        if not vecfilepath.is_file():
            log.debug(f"No .vec file found at '{str(vecfilepath)}'")
            if not rawfilepath.is_file():
                log.debug(f"No raw (.bin/.zip/.gz) file found at '{str(rawfilepath)}'")
                zipfilepath = download(DEFAULT_RAW_URLS[algoname])
                rawfilepath = Path(zipfilepath).rename(rawfilepath)
            log.debug(f"Unzipping raw file '{rawfilepath}'")
            filepaths = unzip_files(rawfilepath)
            vecfilepath = filepaths[-1]
            for vecfilepath in filepaths:
                if vecfilepath.lower().endswith('.vec'):
                    break
            log.debug(f"New vecfilepath='{vecfilepath}'")
            vecfilepath = Path(vecfilepath).rename(DATA_DIR / Path(DEFAULT_VEC_FILENAMES[algoname]))
        df = load_vecs_df(vecfilepath, encoding='utf-8')
        hdf5filepath = df_to_hdf5(df, filepath=hdf5filepath)
    return load_hdf5_df(hdf5filepath)


def load_glove_df(num_vecs=None, algoname='glove'):
    """ Load a word embeddings from a fasttext hdf5 file and memory-map to a DataFrame """
    hdf5filepath = DATA_DIR / Path(DEFAULT_HDF5_FILENAMES[algoname])
    if not hdf5filepath.is_file():
        log.debug(f"No hdf5 file found at '{str(hdf5filepath)}'")
        vecfilepath = DATA_DIR / Path(DEFAULT_VEC_FILENAMES[algoname])
        rawfilepath = DATA_DIR / Path(DEFAULT_RAW_FILENAMES[algoname])
        if not vecfilepath.is_file():
            log.debug(f"No .vec file found at '{str(vecfilepath)}'")
            if not rawfilepath.is_file():
                log.debug(f"No raw (.bin/.zip/.gz) file found at '{str(rawfilepath)}'")
                zipfilepath = download(DEFAULT_RAW_URLS[algoname])
                rawfilepath = Path(zipfilepath).rename(rawfilepath)
            log.debug(f"Unzipping raw file '{rawfilepath}'")
            filepaths = unzip_files(rawfilepath)
            vecfilepath = filepaths[-1]
            for vecfilepath in filepaths:
                if vecfilepath.lower().endswith('.vec'):
                    break
            log.debug(f"New vecfilepath='{vecfilepath}'")
            vecfilepath = Path(vecfilepath).rename(DATA_DIR / Path(DEFAULT_VEC_FILENAMES[algoname]))
        df = load_vecs_df(vecfilepath, encoding='utf-8')
        hdf5filepath = df_to_hdf5(df, filepath=hdf5filepath)
    return load_hdf5_df(hdf5filepath)


# def load_word2vec_df(url=None):
#     """ Download the Google News word2vec pretrained word vectors """
#     filepath = download_word2vec_if_necessary(url=None)
#     return word2vec.read_bin(filepath)


def load_word2vec_df(num_vecs=None, algoname='word2vec'):
    """ Load a word embeddings from a fasttext hdf5 file and memory-map to a DataFrame """
    hdf5filepath = DATA_DIR / Path(DEFAULT_HDF5_FILENAMES[algoname])
    if not hdf5filepath.is_file():
        log.debug(f"No hdf5 file found at '{str(hdf5filepath)}'")
        vecfilepath = DATA_DIR / Path(DEFAULT_VEC_FILENAMES[algoname])
        rawfilepath = DATA_DIR / Path(DEFAULT_RAW_FILENAMES[algoname])
        if not vecfilepath.is_file():
            log.debug(f"No .vec file found at '{str(vecfilepath)}'")
            if not rawfilepath.is_file():
                log.debug(f"No raw (.bin/.zip/.gz) file found at '{str(rawfilepath)}'")
                zipfilepath = download(DEFAULT_RAW_URLS[algoname])
                rawfilepath = Path(zipfilepath).rename(rawfilepath)
            log.debug(f"Unzipping raw file '{rawfilepath}'")
            filepaths = unzip_files(rawfilepath)
            vecfilepath = filepaths[-1]
            for vecfilepath in filepaths:
                if vecfilepath.lower().endswith('.vec'):
                    break
            log.debug(f"New vecfilepath='{vecfilepath}'")
            vecfilepath = Path(vecfilepath).rename(DATA_DIR / Path(DEFAULT_VEC_FILENAMES[algoname]))
        df = load_vecs_df(vecfilepath, encoding='utf-8')
        hdf5filepath = df_to_hdf5(df, filepath=hdf5filepath)
    return load_hdf5_df(hdf5filepath)


def load_embeddings(algoname='word2vec', num_vecs=None):
    """ Load a word embeddings from a fasttext hdf5 file and memory-map to a DataFrame """
    hdf5filepath = DATA_DIR / Path(DEFAULT_HDF5_FILENAMES[algoname])
    if not hdf5filepath.is_file():
        log.debug(f"No hdf5 file found at '{str(hdf5filepath)}'")
        vecfilepath = DATA_DIR / Path(DEFAULT_VEC_FILENAMES[algoname])
        rawfilepath = DATA_DIR / Path(DEFAULT_RAW_FILENAMES[algoname])
        if not vecfilepath.is_file():
            log.debug(f"No .vec file found at '{str(vecfilepath)}'")
            if not rawfilepath.is_file():
                log.debug(f"No raw (.bin/.zip/.gz) file found at '{str(rawfilepath)}'")
                zipfilepath = download(DEFAULT_RAW_URLS[algoname])
                rawfilepath = Path(zipfilepath).rename(rawfilepath)
            log.debug(f"Unzipping raw file '{rawfilepath}'")
            filepaths = unzip_files(rawfilepath)
            vecfilepath = filepaths[-1]
            for vecfilepath in filepaths:
                if vecfilepath.lower().endswith('.vec'):
                    break
            log.debug(f"New vecfilepath='{vecfilepath}'")
            vecfilepath = Path(vecfilepath).rename(DATA_DIR / Path(DEFAULT_VEC_FILENAMES[algoname]))
        df = load_vecs_df(vecfilepath, encoding='utf-8')
        hdf5filepath = df_to_hdf5(df, filepath=hdf5filepath)
    return load_hdf5_df(hdf5filepath)


load_word2vec = load_word2vec_df
load_glove = load_glove_df
load_fasttext = load_fasttext_df
