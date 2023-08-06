""" Tokenizers, case-folding, normalizers, name-standardizers

## Tokenizer

See NLPiA 2e Chapter 2

## Unicode preprocessing

See https://stackoverflow.com/questions/10294032/python-replace-typographical-quotes-dashes-etc-with-their-ascii-counterparts
"""

import re

from .re_patterns import RE_FINDALL_TOKENS


def normalize_unicode(text):
    """ Normalize embellished unicode characters (combine embellishments with char) """
    return unicodedata.normalize('NFKC', text)


def tokenize(text, pattern=RE_FINDALL_TOKENS):
    r""" Split English text into words, ignoring only 1 internal punctuation"

    default pattern = r'\w+(?:\'\w+)?|[^\w\s]'

    returns list(re.findall(pattern, text))
    """
    return list(generate_tokens(text=text, pattern=pattern))


def generate_tokens(text, pattern=RE_FINDALL_TOKENS):
    r""" Split English text into words, ignoring only 1 internal punctuation"

    default pattern = r'\w+(?:\'\w+)?|[^\w\s]'

    returns list(re.findall(pattern, text))
    """
    return re.findall(pattern, text)


import unicodedata  # noqa


def simple_normalize(s):
    transl_table = dict(
        [(ord(x), ord(y)) for x, y in zip(u"‘’´“”–-", u"'''\"\"--")])
    return s.translate(transl_table)


def unicode_character_name(char):
    try:
        return unicodedata.name(char)
    except ValueError:
        return None


def quotes_hyphens_dashes():
    """ Find all quotes, dashes, and hyphens among the unicode charset

    >>> mapping = quotes_hyphens_dashes()
    >>> ' '.join(mapping['quotes'])
    '" « » ‘ ’ ‚ ‛ “ ” „ ‟ ‹ › ❛ ❜ ❝ ❞ ❟ ❠ ❮ ❯ ⹂ 〝 〞 〟 ＂'
    >>> ' '.join(mapping['hyphens'])
    '- ­ ֊ ᐀ ᠆ ‐ ‑ ‧ ⁃ ⸗ ⸚ ⹀ ゠ ﹣ －'
    >>> ' '.join(mapping['dashes'])
    '‒ – — ⁓ ⊝ ⑈ ┄ ┅ ┆ ┇ ┈ ┉ ┊ ┋ ╌ ╍ ╎ ╏ ⤌ ⤍ ⤎ ⤏ ⤐ ⥪ ⥫ ⥬ ⥭ ⩜ ⩝ ⫘ ⫦ ⬷ ⸺ ⸻ ⹃ 〜 〰 ︱ ︲ ﹘ 💨'
    """
    # Generate all Unicode characters with their names
    unicode_chars = []
    for n in range(0, 0x10ffff):    # Unicode planes 0-16
        char = chr(n)               # Python 3
        # char = unichr(n)           # Python 2
        name = unicode_character_name(char)
        if name:
            unicode_chars.append((char, name))

    mapping = dict(
        apostrophes="‘’‛❛❜",
        commas="‚,",
        quotes=[
            c for c, name in unicode_chars if 'QUOTATION MARK' in name],
        hyphens=[
            c for c, name in unicode_chars if 'HYPHEN' in name],
        dashes=[
            c for c, name in unicode_chars
            if 'DASH' in name and 'DASHED' not in name]
    )
    return mapping
