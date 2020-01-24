import re
from math import log
from typing import Any, Dict, Generic, List, Optional, TypeVar, Tuple, Set


T = TypeVar('T')


class Hit(Generic[T]):
    def __init__(self, doc: T, score: float) -> None:
        self.doc = doc
        self.score = score


class Results(Generic[T]):
    def __init__(self, max_score: float, hits: List[Hit[T]]):
        self.max_score = max_score
        self.hits = hits

    @classmethod
    def from_list(cls, results: List[Any]) -> 'Results':
        max_score = results[0]['score'] if results else None
        return cls(max_score, hits=results)


class SearchManager(Generic[T]):
    def __init__(self, mappings):
        self.mappings = mappings
        self.index: Dict[str, List[Tuple[int, float]]] = {}
        self.documents: List[T] = []

    def bulk_add_documents(self, documents: List[T]):
        for i, doc in enumerate(documents):
            analyses = self.mappings.analyze(doc)
            for token, importance in analyses:
                if token in self.index:
                    self.index[token].append((i, importance))
                else:
                    self.index[token] = [(i, importance)]
        self.documents = documents

    def search(self, query: str, latlng: Optional[Tuple[float, float]] = None) -> Results:
        matches: Set[int] = set()
        first_term = True
        terms = re.split('[ -]', query)
        weights: Dict[int, float] = {}  # store weights to combine them later
        for term in terms:
            docs_for_term = self.index.get(term, [])
            if docs_for_term:
                # idf reduces the importance of common words like `Saint` or `North`
                idf = 1 + log(len(self.documents) / (len(docs_for_term) + 1))
                for i, importance in docs_for_term:
                    weights[i] = idf * importance
            doc_idxs_for_term = [doc[0] for doc in docs_for_term]
            if first_term:
                matches = set(doc_idxs_for_term)
                first_term = False
            else:
                matches = set(doc_idxs_for_term).intersection(matches)
        results = []
        for i in matches:
            doc = self.documents[i]
            score = weights[i]

            boost = 1
            for booster in self.mappings.boosts:
                boost *= booster(latlng, doc, score) if latlng else 1

            results.append({
                'score': score * boost,
                'doc': doc,
            })

        results.sort(key=lambda r: r['score'], reverse=True)
        return Results.from_list(results)
