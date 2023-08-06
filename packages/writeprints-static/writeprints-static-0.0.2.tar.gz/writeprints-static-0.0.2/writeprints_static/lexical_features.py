"""This module is used to extract lexical features for the WriteprintsStatic class.

For every feature, we document the description of the original feature, the technical details we use to recover it, and
known differences between the original feature and our engineering.
"""
import string
import numpy as np

# fmt: off
SPECIALS = ['~', '@', '#', '$', '%', '^', '&', '*', '-', '_', '=', '+', '>', '<', '[', ']', '{', '}', '/', '\\', '|']
BIGRAMS = ['th', 'he', 'in', 'er', 'an', 're', 'on', 'at', 'en', 'nd', 'ed', 'or', 'es', 'ti', 'te', 'it', 'is', 'st',
           'to', 'ar', 'of', 'ng', 'ha', 'al', 'ou', 'nt', 'as', 'hi', 'se', 'le', 've', 'me', 'co', 'ne', 'de', 'ea',
           'ro', 'io', 'ri']
TRIGRAMS = ['the', 'and', 'ing', 'ion', 'ent', 'tio', 'her', 'for', 'hat', 'tha', 'his', 'ter', 'ere', 'ati', 'ate',
            'was', 'all', 'ver', 'ith', 'thi']
# fmt: on


def total_words_extractor(word_tokens):
    """total_words

    Counts the number of words in the text.

    A "word" in this context is any token.text in the spacy doc instance which does
    not match the regular expression '[^\w]+$'.

    Known differences with Writeprints Static feature "total words": None.

    Note that there are many different English-language tokenizers.

    Args:
        word_tokens: List of lists of token.text in spaCy doc instances.

    Returns:
        Number of words in the document.
    """
    total_words = [[len(word_token)] for word_token in word_tokens]
    label = ["total_words"]

    return np.array(total_words), label


def avg_word_length_extractor(word_tokens):
    """avg_word_length

    Counts the average number of characters for words in the text.

    The length the concatenation of all words over "total words" is counted.

    Known differences with Writeprints Static feature "average word length": None.

    Args:
        word_tokens: List of lists of token.text in spaCy doc instances.

    Returns:
        Average length of words in the document.
    """
    avg_word_length = [
        [sum([len(word) for word in word_token]) / len(word_token)]
        for word_token in word_tokens
    ]
    label = ["avg_word_length"]

    return np.array(avg_word_length), label


def short_words_extractor(word_tokens):
    """short_words

    Counts the number of words shorter than four characters in the text.

    Known differences with Writeprints Static feature "number of short words": None.

    Args:
        word_tokens: List of lists of token.text in spaCy doc instances.

    Returns:
        The number of short words in the document.
    """
    short_words = [
        [len([word for word in word_token if len(word) < 4])]
        for word_token in word_tokens
    ]
    label = ["short_words"]

    return np.array(short_words), label


def total_chars_extractor(raws):
    """total_chars

    Counts total number of characters in the text.

    All characters including letters, spaces, and punctuations are counted, leaving spaces after the last valid
    non-space character discarded.

    Known differences with Writeprints Static feature "total char": The total characters of a text is vague when
    it comes to the fact that spaces have length (and even trickier that len('\t')==1 but len('  ')==2). Here we
    consider the "partial with-space" version of this feature because we believe the use of spaces is a useful feature.
    But the space after the last non-space character is more like an artifact than a useful indicator.

    Args:
        raws: List of documents.

    Returns:
        The partial with-space length of the text.
    """
    total_chars = [[len(raw.rstrip())] for raw in raws]
    label = ["total_chars"]

    return np.array(total_chars), label


def digits_ratio_extractor(raws):
    """digits_ratio

    Percentage of digits over all characters in a given text.

    Known differences with Writeprints Static feature "percentage of digits": None.

    Args:
        raws: List of documents.

    Returns:
        Percentage of digits over all characters in the document.
    """
    digits_ratio = [
        [len([char for char in raw if char.isdigit()]) / len(raw.rstrip())]
        for raw in raws
    ]
    label = ["digits_ratio"]

    return np.array(digits_ratio), label


def uppercase_ratio_extractor(raws):
    """uppercase_ratio

    Percentage of uppercase letters out of the total characters in a given text.

    Known differences with Writeprints Static feature "percentage of uppercase letters": None.

    Args:
        raws: List of documents.

    Returns:
        Percentage of uppercase letters over all characters in the document.
    """
    uppercase_ratio = [
        [len([char for char in raw if char.isupper()]) / len(raw.rstrip())]
        for raw in raws
    ]
    label = ["uppercase_ratio"]

    return np.array(uppercase_ratio), label


def special_char_extractor(raws):
    """special_char_

    Frequencies of 21 special characters in the text.

    The special characters are tilde, at, hashtag, dollar sign, percent sign, caret, ampersand, asterisk, hyphen,
    underline, equals sign, plus, greater than, less than, left bracket, right bracket, left brace", right brace, slash,
    backslash, and vertical bar.

    Known differences with Writeprints Static feature "occurrence of special characters": None.

    Args:
        raws: List of documents.

    Returns:
        Frequencies of special characters in the document.
    """
    special_char_ = [[raw.count(special) for special in SPECIALS] for raw in raws]
    # fmt: off
    label = ['special_char_' + special_name for special_name in ['tilde', 'at', 'hashtag', 'dollar_sign',
                                                                 'percent_sign', 'caret', 'ampersand', 'asterisk',
                                                                 'hyphen', 'underline', 'equals_sign', 'plus',
                                                                 'greater_than', 'less_than', 'left_bracket',
                                                                 'right_bracket', 'left_brace', 'right_brace', 'slash',
                                                                 'backslash', 'vertical_bar']]
    # fmt: on

    return np.array(special_char_), label


def letter_extractor(raws):
    """letter_

    Frequencies of 26 English letters in a given text, case insensitive.

    Known differences with Writeprints Static feature "letter frequency": None.

    Args:
        raws: List of documents.

    Returns:
        Frequencies of English letters in the document.
    """
    letter_ = [[raw.count(letter) for letter in string.ascii_lowercase] for raw in raws]
    label = ["letter_" + letter for letter in string.ascii_lowercase]

    return np.array(letter_), label


def digit_extractor(raws):
    """digit_

    Frequencies of 10 digits in a given text.

    Known differences with Writeprints Static feature "digit frequency": None.

    Args:
        raws: List of documents.

    Returns:
        Frequencies of digits in the document.
    """
    digit_ = [[raw.count(digit) for digit in string.digits] for raw in raws]
    label = ["digit_" + digit for digit in string.digits]

    return np.array(digit_), label


def bigram_extractor(word_tokens):
    """bigram_

    39 common letter bigrams in the text, case insensitive, within words.

    Known differences with Writeprints Static feature "percentage of common bigrams": The most frequent 39 character
    bigrams in the Brown Corpus are used as an alternative since we cannot find the original bigrams.

    Args:
        word_tokens: List of lists of token.text in spaCy doc instances.

    Returns:
        Frequencies of character bigrams in the document.
    """
    all_bigrams = [
        sum(
            [
                [(word[x : x + 2]) for x in range(len(word) - (2 - 1))]
                for word in word_token
            ],
            [],
        )
        for word_token in word_tokens
    ]
    bigram_ = [
        [all_bigram.count(bigram) for bigram in BIGRAMS] for all_bigram in all_bigrams
    ]
    label = ["bigram_" + bigram for bigram in BIGRAMS]

    return np.array(bigram_), label


def trigram_extractor(word_tokens):
    """trigram_

    20 common letter trigrams in the text, case insensitive, within words.

    Known differences with Writeprints Static feature "percentage of common trigrams": The most frequent 20 character
    trigrams in the Brown Corpus are used as an alternative since we cannot find the original trigrams.

    Args:
        word_tokens: List of lists of token.text in spaCy doc instances.

    Returns:
        Frequencies of character trigrams in the document.
    """
    all_trigrams = [
        sum(
            [
                [(word[x : x + 3]) for x in range(len(word) - (3 - 1))]
                for word in word_token
            ],
            [],
        )
        for word_token in word_tokens
    ]
    trigram_ = [
        [all_trigram.count(trigram) for trigram in TRIGRAMS]
        for all_trigram in all_trigrams
    ]
    label = ["trigram_" + trigram for trigram in TRIGRAMS]

    return np.array(trigram_), label


def hapax_legomena_ratio_extractor(word_tokens):
    """hapax_legomena_ratio

    Counts word token occurs only once over total words in the text.

    Words of different form are counted as different word tokens. The token.text presents only once in spaCy's doc
    instance over "total_words" is counted.

    Known differences with Writeprints Static feature "Ratio of hapax legomena": None.

    Args:
        word_tokens: List of lists of token.text in spaCy doc instances.

    Returns:
        Ratio of hapax legomena in the document.
    """
    hapax_legomena_ratio = [
        [
            len([word for word in word_token if word_token.count(word) == 1])
            / len(set([word for word in word_token]))
        ]
        for word_token in word_tokens
    ]
    label = ["hapax_legomena_ratio"]

    return np.array(hapax_legomena_ratio), label


def dis_legomena_ratio_extractor(word_tokens):
    """dis_legomena_ratio

    Counts word token occurs twice over total words in the text.

    Words of different form are counted as different word tokens. The token.text presents twice in spaCy's doc instance
    over "total_words" is counted.

    Known differences with Writeprints Static feature "Ratio of dis legomena": None.

    Args:
        word_tokens: List of lists of token.text in spaCy doc instances.

    Returns:
        Ratio of dis legomena in the document.
    """
    dis_legomena_ratio = [
        [
            len([word for word in word_token if word_token.count(word) == 2])
            / (2 * len(set([word for word in word_token])))
        ]
        for word_token in word_tokens
    ]
    label = ["dis_legomena_ratio"]

    return np.array(dis_legomena_ratio), label
