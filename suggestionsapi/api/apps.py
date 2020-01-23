import os

from django.apps import AppConfig
from django.conf import settings

from search.manager import SearchManager
from search.geonames_cities_mappings import GeonamesCitiesMappings
from search.tsv_documents_loader import TsvDocumentsLoader


search_manager = SearchManager(mappings=GeonamesCitiesMappings())


class SuggestionsConfig(AppConfig):
    name = 'api'
    verbose_name = 'Location Suggestions'
    def ready(self):
        loader = TsvDocumentsLoader(os.path.join(settings.PROJECT_DIR, 'data/cities_canada-usa.tsv'))
        loader.load_documents()
        
        search_manager.bulk_add_documents(loader.documents)
        
        print(len(loader.documents), "Documents loaded into Index")
