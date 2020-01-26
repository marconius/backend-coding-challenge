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
        # idf reduces the importance of common words like `Saint` or `North`
        # these are calculated during indexing
        self.idfs: Dict[str, float] = {}
        self.documents: List[T] = []

    def bulk_add_documents(self, documents: List[T]):
        if len(documents) == 0:
            return
        for i, doc in enumerate(documents):
            analyses = self.mappings.analyze(doc)
            for token, importance in analyses:
                num_docs_for_term = 1
                if token in self.index:
                    docs = self.index[token]
                    docs.append((i, importance))
                    num_docs_for_term = len(docs)
                else:
                    self.index[token] = [(i, importance)]
                self.idfs[token] = 1 + log(len(documents) / (num_docs_for_term + 1))
        self.documents = documents

    def search(self, query: str, latlng: Optional[Tuple[float, float]] = None) -> Results:
        position_of_matched_documents: Set[int] = set()
        first_term = True
        terms = re.split('[ -]', query.lower())

        # We store weights to combine them later. This makes it easier to use set, which in turn
        # makes it easier to do `term1` AND `term2` as we build set of matches.
        weights: Dict[int, float] = {}

        for term in terms:
            docs_for_term = self.index.get(term, [])
            if docs_for_term:
                for i, importance in docs_for_term:
                    weights[i] = self.idfs[term] * importance
            doc_idxs_for_term = [doc[0] for doc in docs_for_term]
            if first_term:
                position_of_matched_documents = set(doc_idxs_for_term)
                first_term = False
            else:
                position_of_matched_documents = set(
                    doc_idxs_for_term
                ).intersection(position_of_matched_documents)

        results = []
        for i in position_of_matched_documents:
            doc = self.documents[i]
            score = weights[i]

            boost = 1
            for booster in self.mappings.boosts:
                boost *= booster(latlng, doc) if latlng else 1

            results.append({
                'score': score * boost,
                'doc': doc,
            })

        results.sort(key=lambda r: r['score'], reverse=True)
        return Results.from_list(results)
