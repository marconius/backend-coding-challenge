from abc import ABCMeta, abstractmethod
from typing import Dict, List, Optional, Tuple


class Analyzer(metaclass=ABCMeta):
    @abstractmethod
    def analyze(self, value: str) -> List[str]: pass


class KeywordAnalyzer(Analyzer):
    
    def analyze(self, value: str) -> List[str]:
        return [value]



class AutocompleteAnalyzer(Analyzer):
    
    def analyze(self, value: str) -> List[str]:
        return []


class ListAnalyzer(Analyzer):
    
    def analyze(self, value: str) -> List[str]:
        return []


class NoopAnalyzer(Analyzer):
    
    def analyze(self, value: str) -> List[str]:
        return []
