# constants.py
from collections.abc import Mapping
from collections import OrderedDict
import datetime
import logging
from pathlib import Path
import pkg_resources
from pytz import timezone
import shutil
import string
from urllib.request import urlretrieve

import numpy as np
import pandas as pd

log = logging.getLogger(__name__)


PKG_DIR = Path(__file__).absolute().resolve().parent
PKG_NAME = PKG_DIR.name
SRC_DIR = PKG_DIR.parent
REPO_DIR = SRC_DIR.parent

DATA_DIR_NAME = '.nlpia2-data'
HOME_DIR = Path.home()
DATA_DIR = HOME_DIR / DATA_DIR_NAME


def get_version():
    """ Look within setup.cfg for version = ... and within setup.py for __version__ = """
    version = '0.0.0'
    try:
        return pkg_resources.get_distribution(PKG_NAME)
    except Exception as e:
        log.error(e)
        log.warning(f"Unable to find {PKG_NAME} version so using {version}")
    return version


# SRC_DIR will be the lib/pythonX.X/site-packages directory if nessvec installed with pip from PyPi
SRC_DIR = PKG_DIR.parent

# REPO_DIR will be either ...
#    1. the parent of site-packages (if pip installed into ananconda3 env):
#       `~/anaconda3/envs/nessvec/lib/python3.8/`
#    OR
#    2. the git local clone of the git repository (if cloned into ~):
#       `~/nessvec/`
REPO_DIR = SRC_DIR.parent


# def get_version():
#     """ Look within setup.cfg for version = ... and within setup.py for __version__ = """
#     try:
#         import nessvec
#         return nessvec.__version__
#     except ImportError:
#         pass

#     try:
#         # setup.cfg
#         with (REPO_DIR / 'setup.cfg').open() as fin:
#             for line in fin:
#                 matched = re.match(r'\s*version\s*=\s*([.0-9abrc])\b', line)
#                 if matched:
#                     return (matched.groups()[-1] or '').strip()
#     except FileNotFoundError:
#         return None
#     except Exception as e:
#         print('ERROR: Unable to find version in setup.cfg.')
#         print(e)

#     try:
#         # setup.py
#         for line in (REPO_DIR / 'setup.py').open():
#             if line.startswith('__version__ = '):
#                 return line[len('__version__ = '):].strip('"').strip("'")
#     except FileNotFoundError:
#         return None
#     except Exception as e:
#         print('ERROR: Unable to find version in setup.py.')
#         print(e)


__version__ = get_version()


log.debug(f'Running {__name__} version {__version__} ...')
# LOGLEVEL = logging.ERROR


############################################################################
# setup DATA_DIR
# TODO: setup.py should handle all this

DATA_CONSTANTS_BASEURL = 'https://gitlab.com/tangibleai/nessvec/-/raw/main/src/nessvec/data/constants'
DATA_CONSTANTS_FILENAMES = [
    'LANG_INFO.csv',
    'LANG_ISO.csv',
    'tlds-from-iana.csv',
    'uri-schemes.xhtml.csv',
]
DATA_CONSTANTS_URLS = [
    f'{DATA_CONSTANTS_BASEURL}/{fn}' for fn in DATA_CONSTANTS_FILENAMES
]

if not (DATA_DIR / 'constants' / 'LANG_ISO.csv').is_file():
    (DATA_DIR / 'constants').mkdir(parents=True, exist_ok=True)
    try:
        shutil.copytree(str(PKG_DIR / 'data'), str(DATA_DIR), dirs_exist_ok=True)
    except FileNotFoundError:
        for fn in DATA_CONSTANTS_FILENAMES:
            url = f'{DATA_CONSTANTS_BASEURL}/{fn}'
            fp = DATA_DIR / 'constants' / fn
            urlretrieve(url, str(fp), show_progress=False, exist_ok=True)

        # the last of the data_dir possibilities is the default
        # copy data files from python package to USER_DATA_DIR

log.debug(f'Storing vectors, models, and benchmark datasets in USER_DATA_DIR={DATA_DIR}')

# TODO: setup.py should handle all this
# setup DATA_DIR
#############################################################################

ANALOGY_URLS = [
    # SAT(acronym for Scholastic Aptitude Test), 5 610 questions divided into 374 semantic classes.
    'https://gitlab.com/tangibleai/word-vector-benchmarks/-/raw/main/word-analogy/monolingual/en/sat.csv',

    # SemEval-2017 Task 2 (Measuring Degrees of Relational Similarity)
    # 10014 questions in 10 classes, 79 subclasses .
    'https://gitlab.com/tangibleai/word-vector-benchmarks/-/raw/main/word-analogy/monolingual/en/semeval.csv',

    # JAIR (Journal of AI Research)
    # 430 questions in 20 semantic classes. Contains words & collocations (e.g. solar system).
    'https://gitlab.com/tangibleai/word-vector-benchmarks/-/raw/main/word-analogy/monolingual/en/jair.csv',

    # MSR(acronym for Microsoft Research Syntactic Analogies), 8000 questions divided into 16 morphological classes.
    'https://gitlab.com/tangibleai/word-vector-benchmarks/-/raw/main/word-analogy/monolingual/en/msr.csv',

    # Semantic-Syntactic Word Relationship Dataset (Google)
    # 19544 questions in 2 classes: morphological (10675) and semantic (8869) relationships) & 10 subclasses
    'https://gitlab.com/tangibleai/word-vector-benchmarks/-/raw/main/word-analogy/monolingual/en/google-analogies.csv',
]


ANALOGY_FILEPATHS = [
    # SAT(acronym for Scholastic Aptitude Test), 5 610 questions divided into 374 semantic classes.
    'en-word-analogy-sat.csv',

    # SemEval-2017 Task 2 (Measuring Degrees of Relational Similarity)
    # 10014 questions in 10 classes, 79 subclasses .
    'en-word-analogy-semeval.csv',

    # JAIR (Journal of AI Research)
    # 430 questions in 20 semantic classes. Contains words & collocations (e.g. solar system).
    'en-word-analogy-jair.csv',

    # MSR(acronym for Microsoft Research Syntactic Analogies), 8000 questions divided into 16 morphological classes.
    'en-word-analogy-msr.csv',

    # Semantic-Syntactic Word Relationship Dataset (Google)
    # 19544 questions in 2 classes: morphological (10675) and semantic (8869) relationships) & 10 subclasses
    'en-word-analogy-google.csv',
]


LARGE_FILES = dict(
    ("-".join(fn.split(".")[0].split("-")[-2:]), dict(url=u, filename=fn))
    for (u, fn) in zip(ANALOGY_URLS, ANALOGY_FILEPATHS)
)

#######################################################
# for nessvec.translation

""" ISO 2-letter abbreviations

>>> import pandas as pd
>>> dfs = pd.read_html('https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes')
>>> dfs[1]
    ISO language name  ...                                              Notes
0           Abkhazian  ...                               also known as Abkhaz
1                Afar  ...                                                NaN
2           Afrikaans  ...                                                NaN
3                Akan  ...         macrolanguage, Twi is tw/twi, Fanti is fat
4            Albanian  ...  macrolanguage, called "Albanian Phylozone" in ...
..                ...  ...                                                ...
178             Xhosa  ...                                                NaN
179           Yiddish  ...  macrolanguage. Changed in 1989 from original I...
180            Yoruba  ...                                                NaN
181    Zhuang, Chuang  ...                                      macrolanguage
182              Zulu  ...                                                NaN

[183 rows x 6 columns]
>>> dfs[1].columns
Index(['ISO language name', '639-1', '639-2/T', '639-2/B', '639-3', 'Notes'], dtype='object')
>>> df = dfs[1]
>>> df[df.columns[:2]]
    ISO language name 639-1
0           Abkhazian    ab
1                Afar    aa
2           Afrikaans    af
3                Akan    ak
4            Albanian    sq
..                ...   ...
178             Xhosa    xh
179           Yiddish    yi
180            Yoruba    yo
181    Zhuang, Chuang    za
182              Zulu    zu

[183 rows x 2 columns]
>>> name2abbrev = list(zip(*df[df.columns[:2]].values.T))
>>> name2abbrev = dict([(n.lower()[:2], a) for (n, a) in name2abbrev])
>>> len(name2abbrev)
104
>>> name2abbrev['po']  # Portuguese
'pt'
>>> abbrev = df[df.columns[1]].values
>>> name2abbrev.update(dict(zip(*[abbrev, abbrev])))
>>> name2abbrev = pd.Series(name2abbrev)
>>> name2abbrev
ab    ab
af    af
ak    ak
al    sq
am    am
      ..
ty    ty
ug    ug
cy    cy
fy    fy
za    za
Length: 205, dtype: object

>>> name2abbrev.name = 'ISO'
>>> name2abbrev.to_csv('LANG_ISO.csv')
>>> n2a = pd.read_csv('LANG_ISO.csv', index_col=0)
"""

LANG_ISO = pd.read_csv(DATA_DIR / 'constants' / 'LANG_ISO.csv', index_col=0)
LANG_ISO = LANG_ISO[LANG_ISO.columns[0]].to_dict()
LANG_INFO = pd.read_csv(DATA_DIR / 'constants' / 'LANG_INFO.csv', index_col=0)


#########################################################
# from qary.constants

LOGGING_FORMAT = '%(asctime)s.%(msecs)d %(levelname)-4s %(filename)s:%(lineno)d %(message)s'
LOGGING_DATEFMT = '%Y-%m-%d:%H:%M:%S'
LOGGING_LEVEL = logging.ERROR
logging.basicConfig(
    format=LOGGING_FORMAT,
    datefmt=LOGGING_DATEFMT,
    level=LOGGING_LEVEL)
# root_logger = logging.getLogger()
log = logging.getLogger(__name__)

# TZ constants
DEFAULT_TZ = timezone('UTC')

MAX_LEN_FILEPATH = 1023  # on OSX `open(fn)` raises OSError('Filename too long') if len(fn)>=1024

# from qary.constants
#########################################################


#####################################################################################
# from pugnlp.constants

tld_iana = pd.read_csv(DATA_DIR / 'constants' / 'tlds-from-iana.csv', encoding='utf8')
tld_iana = OrderedDict(sorted(zip((tld.strip().lstrip('.') for tld in tld_iana.domain),
                                  [(sponsor.strip(), -1) for sponsor in tld_iana.sponsor]),
                              key=lambda x: len(x[0]),
                              reverse=True))
# top 20 in Google searches per day
# sorted by longest first so .com matches before .om (Oman)
tld_popular = OrderedDict(sorted([
    ('com', ('Commercial', 4860000000)),
    ('org', ('Noncommercial', 1950000000)),
    ('edu', ('US accredited postsecondary institutions', 1550000000)),
    ('gov', ('United States Government', 1060000000)),
    ('uk', ('United Kingdom', 473000000)),  # noqa
    ('net', ('Network services', 206000000)),
    ('ca', ('Canada', 165000000)),  # noqa
    ('de', ('Germany', 145000000)),  # noqa
    ('jp', ('Japan', 139000000)),  # noqa
    ('fr', ('France', 96700000)),  # noqa
    ('au', ('Australia', 91000000)),  # noqa
    ('us', ('United States', 68300000)),  # noqa
    ('ru', ('Russian Federation', 67900000)),  # noqa
    ('ch', ('Switzerland', 62100000)),  # noqa
    ('it', ('Italy', 55200000)),  # noqa
    ('nl', ('Netherlands', 45700000)),  # noqa
    ('se', ('Sweden', 39000000)),  # noqa
    ('no', ('Norway', 32300000)),  # noqa
    ('es', ('Spain', 31000000)),  # noqa
    ('mil', ('US Military', 28400000)),
    ], key=lambda x: len(x[0]), reverse=True))

uri_schemes_iana = sorted(pd.read_csv(Path(DATA_DIR) / 'constants' / 'uri-schemes.xhtml.csv',
                                      index_col=0).index.values,
                          key=lambda x: len(str(x)), reverse=True)
uri_schemes_popular = ['chrome-extension', 'example', 'content', 'bitcoin',
                       'telnet', 'mailto',
                       'https', 'gtalk',
                       'http', 'smtp', 'feed',
                       'udp', 'ftp', 'ssh', 'git', 'apt', 'svn', 'cvs']

# these may not all be the sames isinstance types, depending on the env
FLOAT_TYPES = tuple([t for t in set(np.sctypeDict.values()) if t.__name__.startswith('float')] + [float])
FLOAT_DTYPES = tuple(set(np.dtype(typ) for typ in FLOAT_TYPES))
INT_TYPES = tuple([t for t in set(np.sctypeDict.values()) if t.__name__.startswith('int')] + [int])
INT_DTYPES = tuple(set(np.dtype(typ) for typ in INT_TYPES))
NUMERIC_TYPES = tuple(set(list(FLOAT_TYPES) + list(INT_TYPES)))
NUMERIC_DTYPES = tuple(set(np.dtype(typ) for typ in NUMERIC_TYPES))

DATETIME_TYPES = [t for t in set(np.sctypeDict.values()) if t.__name__.startswith('datetime')]
DATETIME_TYPES.extend([datetime.datetime, pd.Timestamp])
DATETIME_TYPES = tuple(DATETIME_TYPES)

DATE_TYPES = (datetime.datetime, datetime.date)

# matrices can be column or row vectors if they have a single col/row
VECTOR_TYPES = (list, tuple, np.matrix, np.ndarray)
MAPPING_TYPES = (Mapping, pd.Series, pd.DataFrame)

# These are the valid dates for all 3 datetime types in python (and the underelying integer nanoseconds)
INT_MAX = INT64_MAX = 2 ** 63 - 1
INT_MIN = INT64_MIN = - 2 ** 63
UINT_MAX = UINT64_MAX = - 2 ** 64 - 1

INT32_MAX = 2 ** 31 - 1
INT32_MIN = - 2 ** 31
UINT32_MAX = - 2 ** 32 - 1

INT16_MAX = 2 ** 15 - 1
INT16_MIN = - 2 ** 15
UINT16_MAX = - 2 ** 16 - 1

# Pandas timestamps can handle nanoseconds? but python datetimestamps cannot.
MAX_TIMESTAMP = pd.Timestamp('2262-04-11 23:47:16.854775', tz='utc')
MIN_TIMESTAMP = pd.Timestamp(datetime.datetime(1677, 9, 22, 0, 12, 44), tz='utc')
ZERO_TIMESTAMP = pd.Timestamp('1970-01-01 00:00:00', tz='utc')

# to_pydatetime() rounds to microseconds, ignoring 807 nanoseconds available in other MAX TIMESTAMPs
MIN_DATETIME = MIN_TIMESTAMP.to_pydatetime()
MAX_DATETIME = MAX_TIMESTAMP.to_pydatetime()
MIN_DATETIME64 = MIN_TIMESTAMP.to_datetime64()
MAX_DATETIME64 = MAX_TIMESTAMP.to_datetime64()
INF = np.inf
NAN = np.nan
NAT = pd.NaT


# str constants
MAX_CHR = MAX_CHAR = chr(127)
APOSTROPHE_CHARS = "'`’"
# Monkey patch so import from constants if you want this:
string.unprintable = '\x00\x01\x02\x03\x04\x05\x06\x07\x08\x0e\x0f' \
    '\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x7f'
ASCII_UNPRINTABLE_CHRS = string.unprintable  # ''.join(chr(i) for i in range(128) if chr(i) not in string.printable)

NULL_VALUES = set(['0', 'None', 'null', "'", ""] + ['0.' + z for z in ['0' * i for i in range(10)]])
# if datetime's are 'repr'ed before being checked for null values sometime 1899-12-30 will come up
NULL_REPR_VALUES = set(['datetime.datetime(1899, 12, 30)'])
# to allow NULL checks to strip off hour/min/sec from string repr when checking for equality
MAX_NULL_REPR_LEN = max(len(s) for s in NULL_REPR_VALUES)

PERCENT_SYMBOLS = ('percent', 'pct', 'pcnt', 'pt', r'%')
FINANCIAL_WHITESPACE = ('Flat', 'flat', ' ', ',', '"', "'", '\t', '\n', '\r', '$')
FINANCIAL_MAPPING = (('k', '000'), ('M', '000000'))

# from pugnlp.constants
#########################################################
