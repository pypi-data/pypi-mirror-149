from nessvec.indexers import Index
import pandas as pd
import sentence_transformers
from nessvec.indexers import tokenize
import numpy as np
index = Index(num_vecs=500_000)
index[0]
index[0:10]
index[0:10].shape
%timeit index[0:10].sum()
%timeit index.data[0:10].sum()
index['word'].dot(index.data[0:100])
index['word'].dot(index.data[0:100].T)
self
self = index
        popular_vectors = self.data[0:top].T
        popular_vectors /= np.linalg.norm(popular_vectors, axis=0)
        word_vector = self[word]
        word_vector /= np.linalg.norm(word_vector)
        word_vector.dot(popular_vectors)
top=100
        popular_vectors = self.data[0:top].T
        popular_vectors /= np.linalg.norm(popular_vectors, axis=0)
        word_vector = self[word]
        word_vector /= np.linalg.norm(word_vector)
        word_vector.dot(popular_vectors)
word = 'word'
        popular_vectors = self.data[0:top].T
        popular_vectors /= np.linalg.norm(popular_vectors, axis=0)
        word_vector = self[word]
        word_vector /= np.linalg.norm(word_vector)
        word_vector.dot(popular_vectors)
        similarities = pd.Series(
            word_vector.dot(popular_vectors),
            index=self.vocab[:top])
similarities.sort()
similarities.sort_values()
similarities.sort_values()[-1]
similarities.sort_values().iloc[-1]
similarities.sort_values().iloc[-1].index
similarities.sort_values().index.iloc[-1]
similarities.sort_values().index.values[-1]
self[similarities.sort_values().index.values[-1]]
self.vocab[similarities.sort_values().index.values[-1]]
self.vocab.index[similarities.sort_values().index.values[-1]]
%hist -o -p -f 2022-03-30-mob-programming-after-party-ch06-extreme-summarization-closest-stopword.hist.py.md
%hist -f 2022-03-30-mob-programming-after-party-ch06-extreme-summarization-closest-stopword.hist.py
