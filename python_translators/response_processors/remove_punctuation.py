from python_translators.response_processors.response_processor import ResponseProcessor
from python_translators.translation_response import TranslationResponse

import copy
import html


class RemovePunctuation(ResponseProcessor):

    """

        sometimes the result returned by Translate with context
        contains some punctuation, e.g.

            sealed,

        which can be seen here: https://github.com/zeeguu-ecosystem/Python-Translators/issues/31

        to address, this we strip such punctuation

    """

    def __init__(self):
        super(RemovePunctuation, self).__init__(name='remove_punctuation')

    def process_response(self, response: TranslationResponse) -> TranslationResponse:
        new_response = copy.deepcopy(response)

        for translation in new_response.translations:
            translation['translation'] = translation['translation'].rstrip(",;. ")

        return new_response
