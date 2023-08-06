# -*- coding: utf-8 -*-
from pkg_resources import get_distribution, DistributionNotFound

try:
    # Change name here if project is renamed and does not equal the package name
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    try:
        from .constants import __version__
        print(f'.constants.__version__ = {__version__}')
    except (ImportError, ModuleNotFoundError):
        try:
            from nessvec.constants import __version__
            print(f'nessvec.constants.__version__ = {__version__}')
        except (ImportError, ModuleNotFoundError) as e:
            print(e)
finally:
    del get_distribution, DistributionNotFound


# from nessvec import constants
# from nessvec import fasttext
# from nessvec import files
# from nessvec import glove
# from nessvec import indexers
# from nessvec import re_patterns
# from nessvec import util
__all__ = [
    'constants',
    'fasttext',
    'files',
    'glove',
    'indexers',
    're_patterns',
    'util',
    # , hypervec
]
# from nessvec import nessvectors as word2vec  # noqa
