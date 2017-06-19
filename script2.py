import asyncio

from python_translators.translation_query import TranslationQuery
from python_translators.factories.microsoft_translator_factory import MicrosoftTranslatorFactory


mt = MicrosoftTranslatorFactory.build(source_language='nl', target_language='en')

loop = asyncio.get_event_loop()
result = loop.run_until_complete(mt.translate(TranslationQuery(
    query='Boom'
)))

print(result)

loop.close()
