from python_translators.translators.composite_parallel_translator import CompositeAsyncTranslator
import asyncio
import time

from python_translators.translators.google_translator import GoogleTranslator
from python_translators.factories.google_translator_factory import GoogleTranslatorFactory
from python_translators.translation_query import TranslationQuery
from python_translators.factories.microsoft_translator_factory import MicrosoftTranslatorFactory
from python_translators.translators.glosbe_translator import GlosbeTranslator

lang_config = dict(
    source_language='nl',
    target_language='en'
)


ca_t = CompositeAsyncTranslator(**lang_config)


google = Composite
ca_t.add_translator(GoogleTranslatorFactory.build(**lang_config))
ca_t.add_translator(MicrosoftTranslatorFactory.build(**lang_config))
ca_t.add_translator(GlosbeTranslator(**lang_config))

response = ca_t.translate(TranslationQuery(
    before_context='De directeur',
    query='treedt af',
    after_context=''
))


print('test.')