from python_translators.response_processors.response_processor import ResponseProcessor
from python_translators.translation_response import TranslationResponse

import copy
import html


class UnescapeHtml(ResponseProcessor):

    def __init__(self):
        super(UnescapeHtml, self).__init__(name='unescape_html')

    def process_response(self, response: TranslationResponse) -> TranslationResponse:
        new_query = copy.deepcopy(response)

        for translation in response.translations:
            translation['translation'] = html.unescape(translation['translation'])

        return new_query
