import argparse
import logging
from pathlib import Path
import time

import numpy as np
import pandas as pd
import psutil               # ??: conda install -c anaconda psutil

from indexers import Index

from .files import load_fasttext_df
from .constants import __version__, DATA_DIR
from .util import download_if_necessary


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def load_fasttext_index():
    df = load_fasttext_df()
    return Index(df)


# for doctests
FASTTEXT_INDEX = load_fasttext_index()


def update_resources_df(resources=None, resources_t0=None):
    if resources is None:
        resources = pd.DataFrame()
    if resources_t0 is None:
        try:
            resources_t0 = resources[resources.columns.values[-1]]
        except KeyError:
            resources_t0 = 0.0
    return resources


def time_and_memory():
    resource_dict = {
        'wall_time': time.time(),
        'process_time': time.process_time(),
        'process_time': time.perf_counter(),
    }
    resource_dict.update(dict(psutil.virtual_memory()._asdict()))
    return pd.Series(resource_dict)


def profile_indexing(vecs, resources=None):
    # keep track of the time and memory used for each big task
    resources = pd.DataFrame() if resources is None else resources

    resources['start'] = time_and_memory()
    index = Index(vecs)
    index.prepare()
    resources['index'] = time_and_memory(resources)

    return index, resources


def profile_query(index, resources=None, analogy='king man queen woman'.split()):
    resources = pd.DataFrame() if resources is None else resources

    if analogy is None:
        analogy = [index.id2tok[i] for i in np.random.randint(len(index), size=(4,))]
    analogy_euc_error = analogy_error(index=index, analogy=analogy)
    resources['query_start'] = time_and_memory()
    index.query(analogy_euc_error.reshape((-1, index.dim)))
    resources['query_finish'] = time_and_memory()


def analogy_error(index, analogy='king man queen woman'.split()):
    wordnums = np.array([index.tok2id[t] for t in analogy])
    vecs = [index[i] for i in wordnums]
    return vecs[0] - vecs[1] - vecs[2] + vecs[3]


def analogy_answer_vector(index, analogy='king man queen woman'.split()):
    wordnums = np.array([index.tok2id[t] for t in analogy])
    vecs = [index[i] for i in wordnums]
    return vecs[0] - vecs[1] + vecs[-1]


def analogy_answer_word(index, analogy='king man queen woman'.split()):
    wordnums = np.array([index.tok2id[t] for t in analogy])
    vecs = [index[i] for i in wordnums]
    return index.query_series((vecs[0] - vecs[1] + vecs[-1]).reshape((-1, index.dim)))


def load_analogies(filepath='google', num_analogies=None, vocab=None):
    # Load an analogy dataset
    filepath = download_if_necessary('analogy-google')
    # TODO: test filepath is None because of download_if_necessary magic causing bug
    return pd.read_csv(filepath, index_col=0, nrows=num_analogies)

    # np.random.seed(451)
    # df_6_analogies = df_analogies.sample(6)
    # log.info(df_6_analogies)
    # for i, row in df_6_analogies.iterrows():
    #     log.info(f'"{row.word1.title()}" is to "{row.word2}" as "{row.word3}" is to "{row.target}"')
    # return df_analogies

    # # "Sink" is to "plumber" as "meat" is to "butcher"
    # # "Plug" is to "insert" as "clamp" is to "grip"
    # # "Noisy" is to "uproar" as "tanned" is to "leather"
    # # "Ceremony" is to "sermon" as "agenda" is to "advertisement"
    # # "Tale" is to "story" as "week" is to "year"
    # #   ^ SEEMS INCORRECT TO ME
    # # "Antiseptic" is to "germs" as "illness" is to "fever"

    # # TODO: search the analogies for NLP/language/linguistics/story/text/writing/computer-related analogies
    # #       subject = vocab['NLP'] + vocab['language'] + vocab['English'] + vocab['computer'] + vocab['AI']
    # df_analogy.sample(6)
    # # ...

    # index.query(np.array([vecs[vocab['king']]]))[0][0]
    # # np.ndarray([2407, 7697, 6406, 1067, 9517, 7610, 600459, 5409, 854338, 5094])

    # vocab.iloc[index.query(np.array([vecs[vocab['king']] - vecs[vocab['man']] + vecs[vocab['woman']]]))[0][0]]
    # # king               2407
    # # queen              6406
    # # kings              7697
    # # monarch            9517
    # # princess          11491
    # # king-            600459
    # # King               1067
    # # prince             7610
    # # queen-consort    623878
    # # queendom         836526
    # # dtype: int64

    # neighbors = index.query(np.array([vecs[vocab['king']] - vecs[vocab['man']] + vecs[vocab['woman']]]))
    # neighbors = pd.DataFrame(
    #     zip(
    #         neighbors[0][0],
    #         neighbors[1][0],
    #         vocab.iloc[neighbors[0][0]].index.values
    #     ),
    #     columns='word_id distance word'.split())


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description="Load word embeddings (GloVe, FastText, Word2Vec) and index them for approximate nearest neighbor search."
    )

    parser.add_argument(
        "--version", action="version",
        version=f"{parser.prog} version {__version__}"
    )

    parser.add_argument(
        "-v", "--verbose", action='count', default=0,
        help='Increase the verbosity (may be repeated, e.g. -vvv',
    )

    parser.add_argument(
        "-n", "--num_vecs", type=int, default=50000,
        help="Number of vectors to index (default=50000)",
    )

    parser.add_argument(
        '-d', '--data_dir', type=Path, default=DATA_DIR,
        help="Location to cache datasets and models (vectors, benchmarks, SpaCy language models)",
    )

    return parser


def main(args=None, num_vecs=100_000, verbosity=0):
    # level = ERRORis50 - verbosity * 10 => verbosity = (ERRORis50 - level) / 10
    log.setLevel(logging.ERROR - verbosity * 10)
    resources = pd.DataFrame()
    resources['start'] = time_and_memory()
    log.info('\n' + str(resources['start'].round(2)))

    # Load the 1Mx300 FastText vectors trained on Wikipedia
    df = load_fasttext_df(num_vecs=num_vecs)
    vecs, vocab = df.values, df.index.values
    resources['load_fasttext_hdf5'] = time_and_memory(resources['start'])
    log.info('\n' + str(resources['load_fasttext_hdf5'].round(2)))

    index, resources = profile_indexing(vecs, resources=resources)
    resources[f'index_{num_vecs}_vecs'] = time_and_memory(resources['load_fasttext_hdf5'])
    log.info('\n' + str(resources[f'index_{num_vecs}_vecs'].round(2)))

    df_analogies = load_analogies()

    log.info(f'Loaded {len(df_analogies)} analogies.')
    results = dict(resources=resources, index=index, vecs=vecs, vocab=vocab, num_vecs=num_vecs)
    globals().update(results)
    return results


if __name__ == '__main__':
    parser = init_argparse()
    args = parser.parse_args()
    LOG_LEVEL = logging.ERROR - args.verbose * 10  # noqa
    logging.getLogger().setLevel(LOG_LEVEL)
    log.info('\n' + str(vars(args)))

    # level = ERRORis50 - verbosity * 10 => verbosity = (ERRORis50 - level) / 10
    results = main(num_vecs=args.num_vecs, verbosity=(logging.ERROR - log.getLevel()) / 10)
