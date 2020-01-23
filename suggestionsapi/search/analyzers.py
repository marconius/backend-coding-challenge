from abc import ABCMeta, abstractmethod
from typing import Dict, List, Optional, Tuple


class Analyzer(metaclass=ABCMeta):
    @abstractmethod
    def analyze(self, value: str) -> List[str]: pass


class KeywordAnalyzer(Analyzer):
    
    def analyze(self, value: str) -> List[str]:
        return [value]


class AutocompleteAnalyzer(Analyzer):
    MIN_GRAM = 3

    def analyze(self, value: str) -> List[str]:
        tokens = []
        words = value.split(' ')
        for word in words:
            length = self.MIN_GRAM
            while length < len(word):
                tokens.append(word[0:length])
                length += 1
            tokens.append(word)
        return tokens


class ListAnalyzer(Analyzer):
    
    def analyze(self, value: str) -> List[str]:
        return value.split(',')


class NoopAnalyzer(Analyzer):
    
    def analyze(self, value: str) -> List[str]:
        return []
