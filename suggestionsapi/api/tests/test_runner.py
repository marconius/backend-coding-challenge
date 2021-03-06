"""Since our app doens't use a database, we need to tell the test runner not to try and load one"""

from django.test.runner import DiscoverRunner


class NoDatabaseTestRunner(DiscoverRunner):

    def get_databases(self, suite):
        pass

    def setup_databases(self, **kwargs):
        pass

    def teardown_databases(self, old_config, **kwargs):
        pass
