from typing import Dict, List, Optional, Tuple, Union

from .analyzers import (
    Analyzer,
    AutocompleteAnalyzer,
    KeywordAnalyzer,
    ListAnalyzer,
    NoopAnalyzer,
)

class GeonamesCitiesMappings():
    
    def analyze(self, document: Dict[str, str]):
        tokens: List[str] = []
        for field in document:
            analyzer = self.get_analyzer(field)
            tokens += analyzer.analyze(document[field])
        return tokens

    def get_analyzer(self, field: str) -> Analyzer:
        if field in ['id', 'feat_class', 'feat_code', 'country']:
            return KeywordAnalyzer()
        if field in ['name','ascii']:
            return AutocompleteAnalyzer()
        if field == 'alt_name':
            return ListAnalyzer()
        return NoopAnalyzer()