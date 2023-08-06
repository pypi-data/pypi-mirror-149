import logging


log = logging.getLogger(__name__)

"""
Create queries for retrieving pages likely to contain pharmaceutical drug names.

>>> from nessvec.translation import build_translator
>>> en2uk = build_translator(source='en', target='uk')
>>> uk2en = build_translator(source='uk', target='en')

>>> bert_translations = [
    ('lists the names of pharmaceutical drugs',
     'перелік найменувань фармацевтичних препаратів'),
    ('lists the names of pharmaceutical drugs',
     'містить назви фармацевтичних препаратів'),
     ]

>>> uk2en(bert_translations[0][0])
['lists the names of pharmaceutical drugs']
>>> en2uk(bert_translations[0][1])
['містить назви фармацевтичних препаратів']

bigtech_translations = [
    ('list of names of pharmaceuticals',
     'перелік найменувань фармацевтичних препаратів'),
    ('medicine',
     'ліки'),
    ('pharmaceutical brand names',
     'назви фармацевтичних брендів'),
    ('pharmaceutical generic names',
     'фармацевтичні генеричні назви'),


"""
DRUG_QUERIES = dict(
    uk=['ліки',
        'назви фармацевтичних брендів',
        'фармацевтичні генеричні назви',
        'перелік найменувань фармацевтичних препаратів',
        'містить назви фармацевтичних препаратів',
        ],
    en=['medicine',
        'pharmaceutical brand names',
        'pharmaceutical generic names',
        'lists the names of pharmaceutical drugs',
        'lists the names of pharmaceutical drugs'
        ]
)

EXCLUDE_HEADINGS = ['See also', 'References', 'Bibliography', 'External links']
TOPIC_TITLES = {
    'chatbot': ['Chatbot', 'ELIZA', 'Turing test', 'AIML', 'Chatterbot', 'Loebner prize', 'Chinese room'],
}


from collections import OrderedDict  # noqa


def split_query_str(query_str):
    if not isinstance(query_str, str):
        return query_str

    queries = []
    for s in ',|;':
        queries = [q.strip() for q in query_str.split(s) if q.strip()]
        if len(queries) > 1:
            break
    return queries


def search(queries=DRUG_QUERIES['en'], results=50, lang='en'):
    """ Search Wikipedia with the query strings listed in queries

    >>> search('hello,world')
    """
    from tqdm import tqdm
    import wikipedia as wiki
    queries = split_query_str(queries)
    wiki.set_lang(lang)

    title_pages = OrderedDict()
    for q in queries:
        title_pages.update(
            OrderedDict(zip(wiki.search(q, results=results), [None] * results)))
    for title in tqdm(title_pages):
        try:
            title_pages[title] = wiki.page(title)
        except wiki.DisambiguationError:
            pass
        except Exception:
            pass
    return title_pages


from tqdm import tqdm  # noqa


def get_pages(title_pages):
    import wikipedia as wiki
    from time import sleep
    for title, page in tqdm(title_pages.items()):
        if page is None:
            try:
                page = wiki.page(title, auto_suggest=False)
            except wiki.DisambiguationError as e:
                page = e
        title_pages[title] = page
        sleep(0.05)
    return title_pages


def get_page_attributes(page, title_pages=None):
    if page is None:
        page = next(iter(title_pages.values))
    page_attributes = [k for k in dir(page) if not k.startswith('_')]
    page_attributes = [
        k for k in page_attributes if type(getattr(page, k)) in (str, int, list)
    ]
    return page_attributes


# page_attributes = get_page_attributes()
PAGE_ATTRIBUTES = ['categories', 'content', 'links', 'original_title',
                   'pageid', 'parent_id', 'references', 'revision_id', 'sections',
                   'summary', 'title', 'url']


def create_pages_data(title_pages, page_attributes=PAGE_ATTRIBUTES):
    """ Convert a dict title: wikipedia.page to a serializable list of dicts, strings,..."""
    from tqdm import tqdm

    pages = OrderedDict()
    for title, page in tqdm(title_pages.items()):
        if title in pages and len(pages[title].get("content", "")) > 1:
            continue
        pages[title] = {}
        for k in dir(page):
            if k not in page_attributes:
                continue
            try:
                pages[title][k] = getattr(page, k)
            except KeyError:
                pages[title][k] = None
    return pages


def dump_json(pages, filename="wikicrawl_dump_json"):
    import json
    filepath = f"{filename}_{len(pages)}.json"

    with open(filepath, "w", encoding="utf8") as fout:
        json.dump(pages, fout, ensure_ascii=False, indent=4)

    return filepath


def crawl_wikipedia(queries=DRUG_QUERIES['en'], search_results=50, lang='en'):
    title_pages = search(queries=queries, results=search_results, lang=lang)
    pages = create_pages_data(title_pages)
    return dump_json(pages)


#####################################################
# FIXME: wiki.py

# pip install urllib3 package!
from urllib.request import urlopen  # noqa

import pandas as pd  # noqa


DEFAULT_NAMESPACE = '-in-ns0'
DEFAULT_LANG = 'en'
DEFAULT_YMD = 'latest'

DUMP_DIR_URL_TEMPLATE = "https://dumps.wikimedia.org/{lang}wiki/{ymd}"
DUMP_TITLE_FILENAME_TEMPLATE = "{lang}wiki-latest-all-titles{namespace}.gz"
DUMP_DIR_URL = DUMP_DIR_URL_TEMPLATE.format(
    lang=DEFAULT_LANG, ymd=DEFAULT_YMD)
DUMP_TITLE_FILENAME_TEMPLATE = DUMP_TITLE_FILENAME_TEMPLATE.format(
    lang=DEFAULT_LANG, namespace=DEFAULT_NAMESPACE)
DUMP_URL_TEMPLATE = '/'.join([DUMP_DIR_URL_TEMPLATE, DUMP_TITLE_FILENAME_TEMPLATE])
DEFAULT_DUMP_URL = DUMP_URL_TEMPLATE.format(
    lang=DEFAULT_LANG, ymd=DEFAULT_YMD, namespace=DEFAULT_NAMESPACE)
log.info(DEFAULT_DUMP_URL)


def download_titles(namespace='main', ymd='latest', lang='en'):
    """ download the latest list of titles from wikimedia data dump

    Input:
      lang='en' | 'es' | ...
      namespace='all' | 'main'
      ymd='latest' or '20220228' or similar
    Returns:
      pd.Series(['Creativity', 'Barak Obama', ...])

    >>> len(df_everything)
    16424821
    >>> len(df_tab_sep)
    16424821
    >>> len(df_no_quoting)
    16424794
    """
    namespace = str(namespace).lower().strip()
    if not namespace or namespace in ('all', '', 'None'):
        namespace = ''
    elif namespace in ('main', 'ns0', '0', '0.0'):
        namespace = '-in-ns0'
    else:
        namespace = f'-in-{namespace}'

    url = DUMP_URL_TEMPLATE.format(
        lang=lang, ymd=ymd, namespace=namespace)
    with urlopen(url) as f:
        df = pd.read_table(
            f,
            sep='\t',  # <1>
            compression="gzip"
        )
    return df[df.columns[0]]
# <1> there are no tabs in the UTF-8 text dump


def crawl_pages(seed, seed_pages=10000, max_depth=10, max_pages=1_000_000, max_rate=200):
    pass


def crawl_categories(category):
    pass


# FIXME
######################################################################
