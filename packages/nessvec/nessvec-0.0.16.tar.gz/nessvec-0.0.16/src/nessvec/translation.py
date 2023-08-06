""" Translation tools based on pretrained multilingual BERT or libretranslate web API

>>> translate = build_translator()
>>> translate('фармацевтичні генеричні назви')
['pharmaceutical generation names']

>>> en2uk = build_translator(source='en', target='uk')
>>> uk2en = build_translator(source='uk', target='en')

>>> uk = en2uk('pharmaceutical generation names')
>>> uk
'фармацевтичні генеричні назви'
>>> uk = en2uk('generic drug names')
>>> uk

>>> uk2en(uk)
['commonly called drugs']
>>> uk = en2uk('common names for drugs')
>>> uk2en(uk)
['commonly used names for drugs']


>>> uk2en(en2uk('list of pharmaceutical drug names'))
['The list of names for pharmaceutical drugs']
>>> uk2en(en2uk('list of pharmaceutical drug name'))
['A list of the names of pharmaceutical drugs']

>>> uk2en('перелік найменувань фармацевтичних препаратів')
['lists the names of pharmaceutical drugs']
>>> en2uk('lists the names of pharmaceutical drugs')
['містить назви фармацевтичних препаратів']
>>> uk2en(en2uk('lists the names of pharmaceutical drugs'))
['contains the name of pharmaceuticals']

# References
- [Nicola Landro's translation tutorial](https://12ft.io/proxy?q=https%3A%2F%2Fz-uo.medium.com%2Flenguage-translations-with-python-5dd745d1067f)
"""
from nessvec.constants import LANG_ISO


DEFAULT_LANG = 'en'
DEFAULT_LANG2 = 'pt'
CANONICAL_ABBREV = {'sp': 'es', 'po': 'pt'}


def standardize_lang(lang):
    abbrev = (lang or '').lower().strip()[:2]
    return LANG_ISO.get(abbrev, abbrev)


def standardize_source_target(*args, source=None, target=None, **kwargs):
    """ Guess what the user intends for source and target when they pass <= 2 lang names

    TODO: can be simplified

    >>> DEFAULT_LANG
    'en'
    >>> DEFAULT_LANG2 = 'uk'
    >>> standardize_source_target()
    ('en', 'uk')
    >>> standardize_source_target(target="uk")
    ('en', 'uk')
    >>> standardize_source_target(source="uk")
    ('uk', 'en')
    >>> standardize_source_target(source="en")
    ('en', 'uk')
    >>> standardize_source_target("es")
    ('es', 'en')
    >>> standardize_source_target(source="es")
    ('es', 'en')
    >>> standardize_source_target(source="ch")
    ('ch', 'en')
    >>> standardize_source_target(source="Chinese")
    ('ch', 'en')
    >>> standardize_source_target("Spanish")
    ('es', 'en')
    >>> standardize_source_target(target="Chinese")
    ('en', 'ch')
    >>> standardize_source_target(source="uk")
    ('uk', 'en')
    >>> standardize_source_target("uk")
    ('uk', 'en')
    """
    if source is not None:
        kwargs['source'] = source
    if target is not None:
        kwargs['target'] = target
    args = [standardize_lang(a) for a in args]
    if len(args) == 2:
        kwargs_too = dict(list(kwargs.items()))
        kwargs['source'], kwargs['target'] = args
        kwargs.update(kwargs_too)
    elif len(args) == 1:
        if 'source' in kwargs:
            kwargs['target'] = args[0]
        elif 'target' in kwargs:
            kwargs['source'] = args[0]
        elif args[0] == DEFAULT_LANG:
            kwargs['target'] = args[0]
        else:
            kwargs['source'] = args[0]
    source = kwargs.get('source')
    target = kwargs.get('target')
    source = standardize_lang(source)
    target = standardize_lang(target)
    if not target:
        if not source:
            source, target = DEFAULT_LANG, DEFAULT_LANG2
        elif source == DEFAULT_LANG:
            target = DEFAULT_LANG2
        else:
            target = DEFAULT_LANG
    if not source:
        if target == DEFAULT_LANG:
            source = DEFAULT_LANG2
        else:
            source = DEFAULT_LANG
    return source, target


def build_translator(*args, source=None, target=None, skip_special_tokens=True, **tok_kwargs):
    source, target = standardize_source_target(*args, source=source, target=target)
    import sentencepiece  # noqa
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

    tokenizer = AutoTokenizer.from_pretrained(
        f'Helsinki-NLP/opus-mt-{source}-{target}')

    def tokenizer_pt(text, return_tensors='pt', **kwargs):
        return tokenizer(text, return_tensors=return_tensors, **kwargs)

    model = AutoModelForSeq2SeqLM.from_pretrained(
        f'Helsinki-NLP/opus-mt-{source}-{target}')

    # model.tokenize = tokenizer_pt

    def translate(text, skip_special_tokens=skip_special_tokens, **kwargs):
        tok_kwargs.update(kwargs)
        input_dict = tokenizer_pt(text, **tok_kwargs)
        encoded_output = model.generate(**input_dict)
        return tokenizer.batch_decode(
            encoded_output, skip_special_tokens=skip_special_tokens)

    # model.translate = translate
    return translate


def tokenize_en(text):
    import spacy
    if tokenize_en.nlp is None:
        tokenize_en.nlp = spacy.load("en_core_web_md")
    return [tok.text for tok in tokenize_en.nlp.tokenizer(text)]


tokenize_en.nlp = None


def tokenize_uk(text):
    import spacy
    if tokenize_uk.nlp is None:
        tokenize_uk.nlp = spacy.load("xx_ent_wiki_sm")
    return [tok.text for tok in tokenize_uk.nlp.tokenizer(text)]


tokenize_uk.nlp = None


"""
>>> import spacy
>>> spacy.cli.download("xx_ent_wiki_sm")
>>> spacy.cli.download("xx_sent_ud_sm")

>>> sent_ud = spacy.load('xx_sent_ud_sm')
>>> ent_wiki = spacy.load('xx_ent_wiki_sm')
>>> spacy_ml = spacy.blank('xx')

>>> from spacy.lang.uk import MultiLanguage  # noqa
"""
