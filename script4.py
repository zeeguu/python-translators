from python_translators.translators.composite_translator import CompositeTranslator
import asyncio
import time

from python_translators.translators.google_translator import GoogleTranslator
from python_translators.factories.google_translator_factory import GoogleTranslatorFactory
from python_translators.translation_query import TranslationQuery
from python_translators.factories.microsoft_translator_factory import MicrosoftTranslatorFactory
from python_translators.translators.glosbe_translator import GlosbeTranslator

lang_config = dict(
    source_language='en',
    target_language='nl'
)


ca_t = CompositeTranslator(**lang_config)

ca_t.add_translator(GoogleTranslatorFactory.build_contextless(**lang_config))
ca_t.add_translator(GoogleTranslatorFactory.build(**lang_config))
ca_t.add_translator(MicrosoftTranslatorFactory.build_with_context(**lang_config))
ca_t.add_translator(GlosbeTranslator(**lang_config))

response = ca_t.translate(TranslationQuery(
    before_context='Dark',
    query='matter',
    after_context=''
))

response2 = ca_t.translate(TranslationQuery(
    before_context='He',
    query='leaves',
    after_context='the building'
))
print('hi')