import re

from abc import ABCMeta, abstractmethod
from math import sqrt
from typing import List, Tuple


class Analyzer(metaclass=ABCMeta):
    @abstractmethod
    def analyze(self, raw_value: str) -> List[Tuple[str, float]]:
        pass


class KeywordAnalyzer(Analyzer):

    def analyze(self, raw_value: str) -> List[Tuple[str, float]]:
        return [(raw_value.lower(), 1.0)]


class AutocompleteAnalyzer(Analyzer):
    MIN_GRAM = 3

    def analyze(self, raw_value: str) -> List[Tuple[str, float]]:
        value = raw_value.lower()
        tokens = [(value, 1.0)]
        words = re.split('[- ]', value)
        # matches in longer fields are less likely to matter
        field_length_norm = 1 / sqrt(len(value))
        for word in words:
            length = self.MIN_GRAM
            while length < len(word):
                token = word[0:length]
                analysis = (token, field_length_norm)
                tokens.append(analysis)
                length += 1
            analysis = (word, field_length_norm)
            tokens.append(analysis)
        return tokens


class ListAnalyzer(Analyzer):

    def analyze(self, raw_value: str) -> List[Tuple[str, float]]:
        return [(token.lower(), 1.0) for token in raw_value.split(',')]


class NoopAnalyzer(Analyzer):

    def analyze(self, raw_value: str) -> List[Tuple[str, float]]:
        return []
