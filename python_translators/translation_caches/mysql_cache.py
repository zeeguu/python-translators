from python_translators.translation_caches.translation_cache import TranslationCache
from python_translators.translation_query import TranslationQuery
from python_translators.translation_response import TranslationResponse

class MySqlCache(TranslationCache):

    instance = None

    def __init__(self, dbname: str, tablename : str, host: str, user: str, password: str):
        self.dbname: str = dbname
        self.tablename: str = tablename
        self.host: str = host
        self.user: str = user
        self.password: str = password

    def store(self, query: TranslationQuery, source_language: str, target_language: str, response: TranslationResponse):
        pass

    def fetch(self, query: TranslationQuery, source_language: str, target_language: str) -> TranslationResponse:
        pass