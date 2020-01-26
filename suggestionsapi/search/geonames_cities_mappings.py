from typing import Any, Dict, FrozenSet, List, Tuple
from math import log, exp

from geopy import distance

from .analyzers import (
    Analyzer,
    AutocompleteAnalyzer,
    KeywordAnalyzer,
    ListAnalyzer,
    NoopAnalyzer,
)


def latlng_boost(latlng: Tuple[float, float], doc: Dict[str, str]):
    """My stab at exponential decay"""
    scale = 50  # km
    decay = 0.5
    decay_norm = log(decay)/scale

    dist = abs(distance.distance(latlng, (doc["lat"], doc["long"])).km)

    boost = exp(decay_norm * max([0.0, float(dist)]))

    return boost


class GeonamesCitiesMappings():
    boosts = [latlng_boost]

    def analyze(self, document: Dict[str, str]) -> FrozenSet[List[Tuple[str, float]]]:
        tokens: List[Any] = []
        for field in document:
            analyzer = self.get_analyzer(field)
            tokens += analyzer.analyze(document[field])
        return frozenset(tokens)

    def get_analyzer(self, field: str) -> Analyzer:
        if field in ['id', 'feat_class', 'feat_code', 'country']:
            return KeywordAnalyzer()
        if field in ['name', 'ascii']:
            return AutocompleteAnalyzer()
        if field == 'alt_name':
            return ListAnalyzer()
        return NoopAnalyzer()
