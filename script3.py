from python_translators.translators.glosbe_translator import GlosbeTranslator
from python_translators.translation_query import TranslationQuery
import asyncio

gt = GlosbeTranslator(source_language='nl', target_language='en')


loop = asyncio.get_event_loop()

result = loop.run_until_complete(gt.translate(query=TranslationQuery(
    query='boom'
)))


print(result)