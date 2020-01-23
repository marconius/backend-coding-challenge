from typing import Any, Dict, List, Optional, Tuple

class Results():
    pass


class SearchManager():

    def __init__(self, mappings):
        self.mappings = mappings
        # self.bulk_add_documents(documents)
        self.index = {}

    def bulk_add_documents(self, documents):
        for i, doc in enumerate(documents):
            tokens = self.mappings.analyze(doc)
            for token in tokens:
                if token in self.index:
                    self.index[token].append(i)
                else:
                    self.index[token] = [i]
        self.documents = documents

    def search(self, q: str, lnglat: Optional[Tuple[float, float]]=None) -> List[Any]:
        # TODO: support more than one token!!!!
        matches = self.index.get(q, [])
        return [self.documents[i] for i in matches]
