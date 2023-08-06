# indexers.py
import logging

import numpy as np
import pandas as pd         # conda install -c conda-forge pandas
import pynndescent as pynn  # conda install -c conda-forge pynndescent

from .text import tokenize

COUNTRY_NAME_EXAMPLES = "Australia USA PNG France China Indonesia India Congo Ethiopia".split()

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


DEFAULT_ALGORITHM = 'fasttext'


class Index(pynn.NNDescent):

    def __init__(self,
                 data,
                 vocab=None,
                 metric='cosine', metric_kwds=None, metric_kwargs=None,
                 tokenizer=tokenize,
                 default=None, oovocab=None, **kwargs):
        """Default distance measure changed from Euclidian to cosine distance

        Augmented pynn.NNDescent index of word vectors (or any other vectors).

        Inputs:
            data or vectors (2D array): table of row vectors to be indexed (each row is typically an embedding)
            vocab (array of str): array of words (str) associated with each vector, self.vocab.index = words, self.vocab.values = rownums
            default (array or None): default OOV vector to return with Index.get(key)

        Index methods and attributes:
            .data (2D np.array or table): vectors stored in NNDescent._raw_data
            .vocab (pd.Series): row numbers of vectors, indexed by words (strings)
            .get_nearest(): get k nearest neighbors for a given vector or word
            .reword_sentence()
            .extreme_summarize( k)
            .query_word()
            .get(word, default=Index.default)
            .default (None or vector) None: new random vector created for each OOV token, vector: fixed for all OOV tokens

        >>> metrics =  (
        ...     "euclidean manhattan chebyshev minkowski canberra braycurtis mahalanobis wminkowski seuclidean cosinecorrelation "
        ...     + "haversine hamming jaccard dice russelrao kulsinski rogerstanimoto sokalmichener sokalsneath yule hellinger wasserstein-1d"
        ...     ).split()
        """
        self.default = default
        # `.data` is canonical for matrix of row-vectors because that's what NNDescent calls it
        if isinstance(data, pd.DataFrame):
            if vocab is None:
                vocab = data.index.values
            data = data.values
        if isinstance(vocab, (pd.Series, pd.Index)):
            if isinstance(vocab.values[0], str):
                vocab = vocab.values
        if vocab is None:
            vocab = np.arange(len(data))

        data = np.array(data)
        vocab = np.array(vocab)

        # if only one vector is provided in an array, reshape it into a row vector
        if len(data.shape) == 1 and 4096 >= len(data) >= 3:
            data = data.reshape(1, -1)

        self.tokenize = tokenizer

        # Here `self.vocab` is a numpy array of words (tokens) or strings
        # Other vocab objects returned by functions in this module are `vocab = tok2id = Series(range(len(words)), index=words)`
        self.vocab = pd.Series(vocab)

        self.tok2id = pd.Series(
            range(len(self.vocab)), index=self.vocab.values)
        self.id2tok = pd.Series(
            self.vocab.index.values, index=self.vocab.values)

        # Compute IDF (inverse document frequency) using Zipf's Law df = 1/rank
        self.id2idf = (1 + np.arange(len(self.id2tok))) / len(self.id2tok)
        self.tok2idf = pd.Series(self.id2idf, index=self.tok2id.index)

        metric_kwargs = metric_kwds if metric_kwds is not None else metric_kwargs
        super().__init__(data=data, metric=metric, metric_kwds=metric_kwargs, **kwargs)
        self.data = self._raw_data
        self.num_vecs, self.num_dims = self.data.shape
        self.setup_oovocab()

    def setup_oovocab(self, tokens=['<OOV>', '<PAD>', '<SOS>', '<EOS>']):
        if not tokens:
            tokens = ['<OOV>', '<PAD>', '<SOS>', '<EOS>']
        self.oovocab = pd.Series(range(len(tokens)), index=tokens)
        self.oovectors = [self.default] if self.default is not None else []
        for tok in self.oovocab[len(self.oovectors):]:
            self.oovectors.append(np.random.randn(self.num_dims))
        self.oovectors = np.array(self.oovectors)
        return self.oovectors

    def append_oovocab(self, token):
        """ Add token to OOV Series of OOV tokens and create new random vector for OOV vector """
        self.oovocab = pd.concat((
            self.oovocab,
            pd.Series(len(self.oovocab), index=[token])
        ))
        self.oovectors = np.concatenate((
            self.oovectors,
            np.random.randn(1, self.num_dims)
        ))
        return self.oovectors[-1]

    def update(self, new_vectors, **kwargs):
        """ Appends additional vectors to _raw_data and words to .vocab using NNDescent.update

        # pseudocode for the internal NNDescent.update() method
        def NNDescent.update(self, X):
            ...
            X = check_array(X, dtype=np.float32, accept_sparse="csr", order="C")
            ...
            self._raw_data = np.vstack([self._raw_data[original_order, :], X])
            ...
            nn_descent(self._raw_data)
        """
        super().update(X=new_vectors, **kwargs)

    def get_similarity(self, word1, word2):
        """ Compute the cosine similarity (normalized dot product) of the vectors for two words

        >>> index = FASTTEXT_INDEX
        >>> index.get_similarity('the', ',')
        0.51132697
        >>> index.get_similarity(',', 'the')
        0.51132697
        """
        cosine_similarity = 0
        return cosine_similarity

    def get(self, key, *args, **kwargs):
        if 'default' in kwargs:
            default = kwargs['default']
            if default is not None:
                self.default = default
        if len(args):
            default = args[0]
            if default is not None:
                if kwargs.get('default') is not None:
                    raise ValueError("You specified a default vector twice: arg[0] and kwargs['default']")
        try:
            return self.__getitem__(key)
        except (KeyError, IndexError):
            try:
                return self.oovectors[self.oovocab[key]]
            except (KeyError, IndexError):
                log.error("Creating new OOV vector and token in self.oovocab and self.oovectors")
        if self.default is not None:
            return self.default
        else:
            return self.append_oovocab(key)

    def get_doc_vector(self, doc: str, use_idf=False):
        """ Find tokens in a str and return the sum of the word vectors for each token

        TODO: for IDF use rank of words to deweight them during the sum according to zipf

        zipf:  y ~ r ^ -1
              word_document_freq ~= 1 / word_rank (ranked by popularity)
        """

        tokens = [t for t in self.tokenize(doc) if t is not None]
        idfs = [1.0] * len(tokens)
        if use_idf:
            idfs = [self.tok2idf[t] if t in self.tok2idf else min(max(len(t) / 16., 1), 1 / len(self.tok2idf))
                    for t in tokens]
        vectors = np.array([
            self.get(tok) * idf for tok, idf in zip(tokens, idfs)])
        vec = vectors.sum(axis=0)
        return vec / len(vectors)

    def get_nearest(self, word_or_vec, k=None, num_neighbors=10, use_idf=False):
        """ Find nearest word vectors to the word or vector provided

        >>> index = FASTTEXT_INDEX
        >>> v1 = index.get('hello')
        >>> v2 = index.get('goodbye')
        >>> index.get_nearest(v1 + v2)
        goodbye      0.082681
        hello        0.087769
        good-bye     0.181120
        ...
        >>> index.get_nearest(
        ...     v1 / np.linalg.norm(v1) + v2 / np.linalg.norm(v2))
        goodbye      0.085206
        hello        0.085207
        good-bye     0.183381
        ...
        (v1 / np.linalg.norm(v1) + v2 / np.linalg.norm(v2))
        >>> index.get_nearest(v3 / np.linalg.norm(v3))
        goodbye      0.085207
        hello        0.085207
        good-bye     0.183381
        """
        if k is None:
            k = num_neighbors
        if k is None:
            k = 10
        if isinstance(word_or_vec, str):
            vector = self.get(word_or_vec)
        else:
            vector = np.array(word_or_vec).reshape(self.num_dims)
        return self.query_series(vector, k=k)

    def get_nearest_popular_word(self, word, max_rank=100, min_rank=0):
        """ Find the most similar popular word (between min_rank and max_rank)

        >>> FASTTEXT_INDEX.get_nearest_popular_word("word")
        "one"
        """
        popular_vectors = self.data[min_rank:max_rank].T
        popular_vectors /= np.linalg.norm(popular_vectors, axis=0)
        word_vector = self[word]
        word_vector /= np.linalg.norm(word_vector)
        similarities = pd.Series(
            word_vector.dot(popular_vectors),
            index=self.vocab.index[min_rank:max_rank])
        return similarities.sort_values().index.values[-1]

    def extreme_summarize(self, doc, k=1, normalize=True, use_idf=True):
        """ Find closest k words to the vector sum of the word vectors in a doc

        The longer the sentence the closer the vector gets to stopwords.
        TODO:
          - filter stopwords
          - subtract the vectors for stopwords
          - add a second importance score or denominator term: proximity to any of the 100 most popular stop words
        >>> index = FASTTEXT_INDEX
        >>> index.extreme_summarize('hello goodbye')
        array(['goodbye'], dtype=object)
        """
        ids, distances = self.get_nearest(
            self.get_doc_vector(doc, normalize=normalize), k=k).index.values
        distances

    def normalize_key(self, key):
        """ Normalize the str associated with a row in Index.data """
        try:
            return key.strip().lower()
        except ValueError:
            return self.vocab[key].strip().lower()

    def tokenize_key(self, key):
        """ Normalize the str associated with a row in Index.data """
        try:
            return key.strip().lower()
        except ValueError:
            return self.vocab[key].strip().lower()

    def query_series(self, *args, **kwargs):
        """ PynnIndex.query but return a pd.Series where the index is the words and values are the similarities """
        qresults = self.query(*args, **kwargs)
        words = self.id2tok[qresults[0][0]]
        distances = qresults[1][0]
        return pd.Series(distances, index=words.index)

    def expand_examples(self, examples=COUNTRY_NAME_EXAMPLES, num_neighbors=10, depth=1):
        """ Given list/set of words find similar word vectors, and recurse for `depth` iterations

        >>> index = FASTTEXT_INDEX
        >>> index.expand_examples('Australia', num_neighbors=2, depth=2)
        {'Adelaide', 'Aussie', 'Australia', 'Australian', 'Melbourne', 'Sydney'}
        """
        if isinstance(examples, str):
            examples = [examples]
        new_examples = set(examples)
        for d in range(depth):
            query_words = list(new_examples)
            for word in query_words:
                new_examples = new_examples.union(self.get_nearest(
                    word,
                    num_neighbors=num_neighbors + 1,
                ).index.values[1:])
                print(word, new_examples)
        return new_examples

    def reword_sentence(self, sent, max_dist=0.2):
        # FIXME: regular for loop instead of list comprehension
        return " ".join(
            [
                self.get_nearest(tok).index.values[1]
                if self.get_nearest(tok).iloc[1] < max_dist
                else tok
                for tok in sent.split()
            ]
        )

    def __getitem__(self, key):
        """ Get a vector by key (word or integer ID) """
        ikey = key
        if isinstance(key, str):
            ikey = self.tok2id[key]
        try:
            return self.data[ikey]
        except (KeyError, IndexError) as e:
            log.info(e)
            log.info(f"Unable to find '{key}' in {self.data.shape} DataFrame of vectors")
        if isinstance(key, str):
            # TODO: normalized_key returns integer row or array of ints
            normalized_key = self.normalize_key(key)
            try:
                return self.data[normalized_key]
            except KeyError as e:
                log.info(e)
                log.info(f"Unable to find '{normalized_key}' in {self.data.shape} DataFrame of vectors")
            tokenized_key = self.tokenize(key.strip())
            return np.array([self.get(k) for k in tokenized_key]).sum(axis=0)

        raise(KeyError(f"Unable to find any of {key} in {self.data.shape[0]}x{self.data.shape[1]} vectors"))

    def query_word(self, word, k=10):
        return self.query(self.data[self.vocab[word]], k=k)

    def query(self, query_data, *args, **kwargs):
        """ Same as pynn.NNDescent.query, but ensures query data array is reshaped appropriately """
        return super().query(np.array(query_data).reshape((-1, self.dim)), *args, **kwargs)


# FIXME: move "augmentation of Index" from Index to here.
def IndexedWordVectors(Index):
    """ Transposed Index such that vectors fit work nicely as columns in a dataframe with column names as tokens/keys """

    def __init__(self, vectors, vocab=None, metric='cosine', metric_kwds=None, metric_kwargs=None, **kwargs):
        """Default distance measure changed from Euclidian to cosine distance

        >>> metrics =  (
        ...     "euclidean manhattan chebyshev minkowski canberra braycurtis mahalanobis wminkowski seuclidean cosinecorrelation "
        ...     + "haversine hamming jaccard dice russelrao kulsinski rogerstanimoto sokalmichener sokalsneath yule hellinger wasserstein-1d"
        ...     ).split()
        """
        vectors = np.array(vectors)
        if len(vectors.shape) == 1 and 4096 >= len(vectors) >= 3:
            vectors = vectors.reshape(1, -1)
        self.vocab = vocab or np.arange(len(vectors))
        self.vocab = pd.Series(vocab)
        metric_kwargs = metric_kwds if metric_kwds is not None else metric_kwargs
        super().__init__(data=vectors, metric=metric, metric_kwds=metric_kwargs, **kwargs)

    # def __init__(self, vocab, vectors=None, normalizer=glove_normalize):
    #     self.normalizer = normalizer
    #     if vectors is None:
    #         self.load()
    #     elif isinstance(vectors, dict):
    #         self.df = pd.DataFrame(vectors)
    #     else:
    #         self.df = pd.DataFrame(vectors, index=(index or range(len(vectors))))

    def get(self, key, default=None):
        if key in self.df.columns:
            return self.df[key]
        return default

    def __getitem__(self, key):
        try:
            return self.df[key]
        except KeyError:
            print(f"Unable to find '{key}' in {self.df.shape} DataFrame of vectors")
        normalized_key = self.normalizer(str(key))
        try:
            return self.df[normalized_key]
        except KeyError:
            print(f"Unable to find '{normalized_key}' in {self.df.shape} DataFrame of vectors")
        raise(KeyError(f"Unable to find any of {set([key, normalized_key])} in self.df.shape DataFrame of vectors"))


# class IndexedVectors:
#     def __init__(self, vectors=None, index=None, normalizer=glove_normalize):
#         self.normalizer = normalizer
#         if vectors is None:
#             self.load()
#         elif isinstance(vectors, dict):
#             self.df = pd.DataFrame(vectors)
#         else:
#             self.df = pd.DataFrame(vectors, index=(index or range(len(vectors))))

#     def load(self, dim=50, size=6):
#         self.df = pd.DataFrame(load_glove(dim=dim, size=size))
#         return self

#     def get(self, key, default=None):
#         if key in self.df.columns:
#             return self.df[key]
#         return default

#     def keys(self):
#         return self.df.columns.values

#     def values(self):
#         return self.df.T.values

#     def iteritems(self):
#         return self.df.T.iterrows()

#     def iterrows(self):
#         return self.df.T.iterrows()
