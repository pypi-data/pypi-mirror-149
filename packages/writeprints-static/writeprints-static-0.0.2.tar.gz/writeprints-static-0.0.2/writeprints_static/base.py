"""This module is used to hold the WriteprintsStatic class.
# writeprints-static

Extracts lexical and syntactic features from texts which are useful in authorship attribution.
"""

import re
import spacy
import warnings
import numpy as np
from scipy.sparse import csr_matrix
from writeprints_static import lexical_features as lex
from writeprints_static import syntactic_features as syn

__version__ = "0.0.2"


class WriteprintsStatic(object):
    """WriteprintsStatic

    The main class does the heavy lifting.

    Attributes:
        raws: A list of raw text fed by user.
        docs: A list of spaCy's doc instances build on self.raws with en_core_web_sm.
        tags: A list of lists of POS, derived from token.pos_ in self.docs.
        word_tokens: A list of lists of word tokens, derived from token.text in self.docs.
        feature_names_: A list of feature names.
    """

    def __init__(self):
        """Initiates WriteprintsStatic."""
        self.docs = None
        self.raws = None
        self.tags = None
        self.word_tokens = None
        self.feature_names_ = None
        self.__version__ = __version__

    def transform(self, input):
        """

        Generates values for WriteprintsStatic instance.

        Note that no explicit check of the input language will be executed, but we do assume the user only feed in
        English documents.

        Args:
            input: A list of English raw texts (in string type).

        Returns:
            A scipy.sparse.csr_matrix instance. Use .toarray() to unpack the return to see the values.

        Raises:
            ValueError: an error if the input is not a list of string or the

        """
        # checks input
        assert isinstance(input, list) and (
            all(isinstance(x, str) for x in input)
        ), "List of strings expected."
        assert all(
            False if len(x) == 0 else True for x in input
        ), "Zero-length string(s) received."
        self.raws = input
        assert all(
            False if len(raw) > 1000000 else True for raw in self.raws
        ), "No string expected longer than 1m characters."
        if any(True if len(raw) > 100000 else False for raw in self.raws):
            warnings.warn(
                "Long string(s) received, runtime could be long.",
                UserWarning,
                stacklevel=2,
            )
        # if a gpu is available
        spacy.prefer_gpu()
        # loads the language model
        nlp = spacy.load("en_core_web_sm")
        # removes unwanted processing procedure for better efficiency
        with nlp.select_pipes(disable="ner"):
            self.docs = [nlp(raw) for raw in self.raws]
        self.word_tokens = [
            [
                token_without_punkt.lower()
                for token_without_punkt in [token.text for token in doc]
                if re.compile(r"[^\w]+$").match(token_without_punkt) is None
            ]
            for doc in self.docs
        ]
        self.tags = [[token.pos_ for token in doc] for doc in self.docs]

        features, labels = zip(
            lex.total_words_extractor(self.word_tokens),
            lex.avg_word_length_extractor(self.word_tokens),
            lex.short_words_extractor(self.word_tokens),
            lex.total_chars_extractor(self.raws),
            lex.digits_ratio_extractor(self.raws),
            lex.uppercase_ratio_extractor(self.raws),
            lex.special_char_extractor(self.raws),
            lex.letter_extractor(self.raws),
            lex.digit_extractor(self.raws),
            lex.bigram_extractor(self.word_tokens),
            lex.trigram_extractor(self.word_tokens),
            lex.hapax_legomena_ratio_extractor(self.word_tokens),
            lex.dis_legomena_ratio_extractor(self.word_tokens),
            syn.function_word_extractor(self.raws),
            syn.pos_extractor(self.tags),
            syn.punctuation_extractor(self.raws),
        )

        features = np.concatenate(features, axis=1)
        self.feature_names_ = sum(labels, [])

        return csr_matrix(features)

    def fit_transform(self, input):
        """See self.transform."""
        return self.transform(input)

    def get_feature_names(self):
        """Returns Writeprints-Static feature names."""
        return self.feature_names_
