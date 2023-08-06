""" NLPIA chapter 6 glove nessvectors

Dependencies:
  * python==3.6.12
  * scann==

References:
  * Stanford NLP's GloVe model and training script [https://github.com/stanfordnlp/glove]
  * Erik Bern's ANN benchmarks with training and testsets: https://github.com/erikbern/ann-benchmarks
  * Spotify's Annoy (with good visualization): [https://github.com/spotify/annoy]
  * Google Research's ScaNN: [pip install scann]()
"""
import os
from collections import OrderedDict

import numpy as np
import pandas as pd


from tqdm import tqdm


def load_glove(filepath):
    # print("Loading Glove Model")
    f = open(filepath, 'r')
    wv = {}
    for i, line in tqdm(enumerate(f)):
        splitLines = line.split()
        word = splitLines[0]
        embedding = np.array([float(value) for value in splitLines[1:]])
        wv[word] = embedding
    # print(len(wv), " words loaded!")
    return wv


wv = load_glove('/home/hobs/Dropbox/data/new/glove.6B.50d.txt')


COMPONENT_WORDS = OrderedDict([
    ('placeness', ('geography Geography geographic geographical geographical_location location ' +
                   'locale locations proximity').split()),
    ('peopleness', 'human Humans homosapiens peole people individuals humankind people men women'.split()),
    ('animalness', 'animal mammal carnivore animals Animal animal_welfare dog pet cats animal'.split()),
    ('conceptness', 'concept concepts idea'.split()),
    ('femaleness', 'female feminine Female females femal woman girl lady'.split()),
    ('maleness', 'masculine macho man boy dude gentleman beard mustache'.split()),
])


def component_vector(words, ndim=None):
    ndim = ndim or len(wv['the'])
    vector = np.zeros(ndim)
    words_found = 0
    for word in words:
        w = word.replace(' ', '_').strip('_')
        try:
            v = wv.get(w, wv[w.lower()])
            vector += v
            words_found += 1
        except KeyError:
            print(f'"{w}"" and "{w.lower()}"" not in word2vec vocab')
    return vector / float(words_found)


COMPONENTS = pd.DataFrame([component_vector(words) for (component, words) in COMPONENT_WORDS.items()],
                          index=[component for (component, words) in COMPONENT_WORDS.items()])


def cosine_similarities(target, components):
    target = 'the'
    components = 'one two the oregon'.split()
    target = wv[target] if isinstance(target, str) else target
    components = np.array([wv[c] for c in components]) if isinstance(components[0], str) else components
    n_vecs, n_dims = components.shape
    target /= np.linalg.norm(target)
    # print(target.shape)
    norms = np.linalg.norm(components, axis=1).reshape(n_vecs, 1)
    norms = norms.dot(np.ones((1, n_dims)))
    # print(norms.shape)
    components /= norms
    # print(components.shape)
    target.dot(components.T)
    return target.dot(components.T)


def nessvector(target, components=COMPONENTS):
    target = wv[target] if isinstance(target, str) else target
    vector = cosine_similarities(target, components.values)
    return pd.Series((vector - vector.mean()) / .15, index=components.index)
""" NLPIA chapter 6 glove nessvectors

Dependencies:
  * python==3.6.12
  * scann==

References:
  * Stanford NLP's GloVe model and training script [https://github.com/stanfordnlp/glove]
  * Erik Bern's ANN benchmarks with training and testsets: https://github.com/erikbern/ann-benchmarks
  * Spotify's Annoy (with good visualization): [https://github.com/spotify/annoy]
  * Google Research's ScaNN: [pip install scann]()
"""


import np


def load_glove(filepath):
    # print("Loading Glove Model")
    f = open(filepath, 'r')
    wv = {}
    for line in f:
        splitLines = line.split()
        word = splitLines[0]
        embedding = np.array([float(value) for value in splitLines[1:]])
        wv[word] = embedding
    # print(len(wv), " words loaded!")
    return wv
