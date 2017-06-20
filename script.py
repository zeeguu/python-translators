import logging

from python_translators.translators.google_translator import GoogleTranslator
from python_translators.factories.google_translator_factory import GoogleTranslatorFactory
from python_translators.translation_query import TranslationQuery

gt = GoogleTranslatorFactory.build(source_language='nl', target_language='en')

tr = gt.translate(TranslationQuery(
    query='hallo'
))

print('Done.')
