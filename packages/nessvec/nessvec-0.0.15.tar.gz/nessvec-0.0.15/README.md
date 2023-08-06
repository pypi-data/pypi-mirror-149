# nessvec

## Install from Source (recommended)

Clone the repository with all the source code and data:

```console
$ git clone git@gitlab.com:tangibleai/nessvec
$ cd nessvec
```

Create a conda environment and install the dependencies:

```console
$ conda create -n nessvec 'python==3.9.7'
$ conda env update -n nessvec -f scripts/environment.yml
$ pip install -e .
```

## Install from PyPi (only tested on Linux)

```console
$ pip install nessvec
```

## Get Started

```python
>>> from nessvec.util import load_glove
>>> w2v = load_glove()
>>> seattle = w2v['seattle']
>>> seattle
array([-2.7303e-01,  8.5872e-01,  1.3546e-01,  8.3849e-01, ...
>>> portland = w2v['portland']
>>> portland
array([-0.78611  ,  1.2758   , -0.0036066,  0.54873  , -0.31474  ,...
>>> len(portland)
50
>>> from numpy.linalg import norm
>>> norm(portland)
4.417...
>>> portland.std()
0.615...

```

```
>>> cosine_similarity(seattle, portland)
0.84...
>>> cosine_similarity(portland, seattle)
0.84...

```

```python
>>> from nessvec.util import cosine_similarity
>>> cosine_similarity(w2v['los_angeles'], w2v['mumbai'])
.5

```

##

