QUERIES = dict(
    medicine='ліки'
)


def load_uk_translator():
    import sentencepiece  # noqa
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-uk-en")
    model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-uk-en")
    return tokenizer, model


from collections import OrderedDict


def get_titles(queries=list(QUERIES.values()), results=50):
    import wikipedia as wiki
    wiki.set_lang("uk")

    title_pages = OrderedDict()
    for query in queries:
        title_pages.update(
            OrderedDict(zip(wiki.search("ліки", results=results), [None] * results)))
    return title_pages


title_pages = get_titles()


def get_pages(title_pages=title_pages):
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


title_pages = get_pages(title_pages)
page = next(iter(title_pages.values))
page_attributes = [k for k in dir(page) if not k.startswith('_')]
page_attributes = [
    k for k in page_attributes if type(getattr(page, k)) in (str, int, list)
]

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
            pages[title][k] = []


def dump_json(pages, filepath=None):
    import json
    if filepath is None:
        filepath = f"ukranian_wikipedia_{len(pages)}.json"

    with open(filepath, "w", encoding="utf8") as fout:
        json.dump(pages, fout, ensure_ascii=False, indent=4)


import spacy
spacy_en = spacy.load("en_core_web_md")


def tokenize_en(text):
    return [tok.text for tok in spacy_en.tokenizer(text)]


from spacy.lang.uk import MultiLanguage
