"""This module is used to extract syntactic features for the WriteprintsStatic class.

For every feature, we document the description of the original feature, the technical details we use to recover it, and
known differences between the original feature and our engineering.
"""

import re
import numpy as np

# fmt: off
FUNCTION_WORDS = ['a', "he's", 'since', 'about', 'highly', 'above', 'him', 'absolutely', 'himself', 'so', 'across',
                  'his', 'some', 'actually', 'hopefully', 'somebody', 'after', 'how', 'somehow', 'again', 'however',
                  'someone', 'against', 'hundred', 'something', 'ahead', 'i', 'somewhat', 'somewhere', "ain't", "i'd",
                  'soon', 'all', 'if', "i'll", 'still', 'along', 'stuff', 'alot', "i'm", 'such', 'also', 'immediately',
                  'ten', 'although', 'in', 'tenth', 'am', 'infinity', 'than', 'among', 'inside', 'that', 'an',
                  'insides', 'thatd', 'and', 'instead', "that'd", 'another', 'into', 'any', 'is', "that'll", 'anybody',
                  'thats', 'anymore', "isn't", "that's", 'anyone', 'it', 'the', 'anything', 'thee', 'anyway', "it'd",
                  'their', 'anywhere', 'item', 'them', 'apparently', 'themselves', 'are', "it'll", 'then', 'its',
                  'there', "aren't", "it's", 'theres', 'around', 'itself', "there's", 'as', 'these', 'at', "i've",
                  'they', 'just', 'atop', 'lack', "they'd", 'away', 'lately', 'back', 'least', "they'll", 'basically',
                  'less', 'be', 'let', "they're", 'became', 'lets', 'because', "let's", "they've", 'become', 'loads',
                  'becomes', 'lot', 'thing', 'becoming', 'third', 'been', 'lots', 'thirty', 'before', 'this', 'behind',
                  'being', 'main', 'those', 'below', 'many', 'thou', 'beneath', 'may', 'though', 'beside', 'maybe',
                  'thousand', 'besides', 'me', 'best', 'might', 'three', 'between', 'through', 'beyond', "might've",
                  'thru', 'billion', 'million', 'thy', 'both', 'mine', 'bunch', 'more', 'till', 'but', 'most', 'to',
                  'by', 'mostly', 'ton', 'can', 'much', 'tons', 'cannot', 'too', 'must', 'total', "can't", 'totally',
                  "must'nt", 'toward', 'clearly', "mustn't", 'trillion', 'completely', 'constantly', "must've", 'truly',
                  'could', 'my', 'myself', "couldn't", 'near', 'twice', 'nearly', 'two', "could've", 'couple',
                  "need'nt", 'under', 'cuz', "needn't", 'underneath', 'definitely', 'unique', 'despite', 'neither',
                  'unless', 'did', 'never', 'until', 'nine', 'unto', "didn't", 'no', 'up', 'difference', 'nobody',
                  'upon', 'do', 'none', 'us', 'does', 'nope', 'usually', 'doesnt', 'nor', 'various', "doesn't", 'not',
                  'very', 'doing', 'nothing', 'wanna', 'done', 'now', 'was', 'dont', 'nowhere', 'wasnt', "don't", 'of',
                  "wasn't", 'doubl', 'off', 'we', 'down', 'often', "we'd", 'dozen', 'on', 'during', 'once', "we'll",
                  'each', 'one', 'were', 'eight', 'ones', "we're", 'either', 'oneself', "weren't", 'eleven', 'only',
                  'else', 'onto', "we've", 'enough', 'or', 'what', 'entire', 'other', 'whatever', 'equal', 'others',
                  'whats', 'especially', 'otherwise', "what's", 'etc', 'ought', 'when', 'even', 'oughta', 'whenever',
                  'eventually', 'where', 'ever', "ought'nt", 'whereas', 'every', "oughtn't", 'wheres', 'everybod',
                  'oughtve', "where's", 'everyone', "ought've", 'whether', 'everything', 'our', 'which', 'example',
                  'ours', 'whichever', 'except', 'ourselves', 'while', 'out', 'who', 'extra', 'outside', 'extremely',
                  'over', "who'd", 'fairly', 'own', 'whole', 'few', 'part', 'fift', 'partly', "who'll", 'first',
                  'perhaps', 'whom', 'firstly', 'piece', 'whose', 'firsts', 'plenty', 'will', 'five', 'plus', 'with',
                  'for', 'primarily', 'within', 'form', 'probably', 'without', 'four', 'quarter', 'wont', 'frequently',
                  'quick', "won't", 'from', 'rarely', 'worst', 'full', 'rather', 'would', 'generally', 'really',
                  'greater', 'remaining', "wouldn't", 'greatest', 'rest', 'wouldve', 'had', 'same', "would've",
                  'second', "hadn't", 'section', 'half', 'seriously', "y'all", 'has', 'seven', 'several', 'yet',
                  "hasn't", 'shall', 'you', 'have', 'havent', "shan't", "you'd", "haven't", 'she', 'having', "she'd",
                  "you'll", "she'll", 'your', "he'd", 'her', "she's", "you're", 'here', 'should', 'yours', 'heres',
                  "here's", "should'nt", "you've", 'hers', "shouldn't", 'zero', 'herself', 'zillion', "should've",
                  'like']
UNIVERSAL_TAGS = ['ADJ', 'ADP', 'ADV', 'AUX', 'CCONJ', 'DET', 'INTJ', 'NOUN', 'NUM', 'PART', 'PRON', 'PROPN', 'PUNCT',
                  'SCONJ', 'SYM', 'VERB', 'X']
PUNCTUATIONS = ["?", "!", ",", ".", "'", '"', ";", ":"]


# fmt: on


def function_word_extractor(raws):
    """function_word_

    Frequencies of 403 common function words in the text.

    The occurrence of each function words used by Jstylo over "total_words". Jstylo's function word list is curated at
    https://github.com/psal/jstylo/blob/master/src/main/resources/edu/drexel/psal/resources/functionWord.txt.

    Known differences with Writeprints Static feature "frequency of function words": Obvious errors in Jstylo's function
    word list are corrected: "loads\t", "billion\t", "somewhere ", and "your " are corrected as "loads", "billion",
    "somewhere", and "your".

    Args:
        raws: List of documents.

    Returns:
        Frequencies of function words in the document.
    """
    function_words_ = [
        [
            len(re.findall(r"\b" + function_word + r"\b", raw.lower()))
            for function_word in FUNCTION_WORDS
        ]
        for raw in raws
    ]
    label = ["function_word_" + function_word for function_word in FUNCTION_WORDS]

    return np.array(function_words_), label


def pos_extractor(tags):
    """pos_

    Frequencies of 17 parts of speech (POS) in the text.

    POS tags are adjective, adposition, adverb, auxiliary, coordinating conjunction, determiner, interjection, noun,
    numeral, particle, pronoun, proper noun, punctuation, subordinating conjunction, symbol, verb, and other.

    The frequency of the universal tagset POS is counted using token.pos_ in spaCy's doc instance.

    Known differences with Writeprints Static feature "frequency of parts of speech tag": The POS tagset used by
    Brennan et al. (2012) has 22 tags. Here a 17-tag universal tagset is used as an alternative since we cannot find the
    original tagset.

    Args:
        tags: List of lists of token.pos_ in spaCy doc instances.

    Returns:
        Frequencies of POS in the document.
    """
    pos_ = [
        [tag.count(universal_tag) for universal_tag in UNIVERSAL_TAGS] for tag in tags
    ]
    label = ["pos_" + universal_tag for universal_tag in UNIVERSAL_TAGS]

    return np.array(pos_), label


def punctuation_extractor(raws):
    """punctuation_

    Frequencies of 8 punctuations in the text.

    Punctuations are question_mark, exclamation, comma, period, single quotes, double quotes, semicolon,
    and colon.

    Though Brennan et al. (2012) Table II states there are 8 punctuations in this category, the immediate following
    feature name only contains 6 punctuations. We refer to Jstylo's punctuation list containing 9 punctuations. The
    punctuation list is curated at
    https://github.com/psal/jstylo/blob/master/src/main/resources/edu/drexel/psal/resources/writeprints_punctuation.txt.
    The last punctuation (asterisk sign) in that list has already been included in the "special_char_" feature set. So
    we use that list with the asterisk omitted.

    Known differences with Writeprints Static feature "frequency and percentage of colon, semicolon, qmark, period,
    exclamation, comma": Only straight single and double quotes are considered. This is a trade-off of desires to
    present the original Writeprints Static and treat curly and straight quotes separately (not to coerce one kind of
    single/double questes mark to the other kind).

    Args:
        raws: List of documents.

    Returns:
        Frequencies of punctuation in the document.
    """
    punctuation_ = [
        [raw.count(punctuation) for punctuation in PUNCTUATIONS] for raw in raws
    ]
    label = [
        "punctuation_" + punctuation_name
        for punctuation_name in [
            "question_mark",
            "exclamation",
            "comma",
            "period",
            "single_quotes",
            "double_quotes",
            "semicolon",
            "colon",
        ]
    ]

    return np.array(punctuation_), label
