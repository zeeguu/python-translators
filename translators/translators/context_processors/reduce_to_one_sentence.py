from context_processor import ContextProcessor
import nltk.data
from translators.language_codes import code_to_full_language
import os.path

NLTK_DATA_PATH = "~/nltk_data/tokenizers/punkt/%(language)s.pickle"


class ReduceToOneSentence(ContextProcessor):
    # Global storage of tokenizers indexed by language code to prevent reloading of tokenizers
    tokenizers = {}

    def __init__(self, language_code):

        # if a tokenizer was already in our global storage
        if language_code in ReduceToOneSentence.tokenizers:
            self.tokenizer = ReduceToOneSentence.tokenizers[language_code]

        else:
            self.tokenizer = ReduceToOneSentence._load_tokenizer(language_code)
            ReduceToOneSentence.tokenizers[language_code] = self.tokenizer

    @staticmethod
    def _load_tokenizer(language_code):
        resource_url = NLTK_DATA_PATH % {'language': code_to_full_language(language_code)}
        resource_url = os.path.expanduser(resource_url)
        print(resource_url)

        return nltk.data.load(resource_url)

    def process_context(self, before_context, query, after_context):
        return {
            'before_context': self.tokenizer.tokenize(before_context)[-1],
            'query': query,
            'after_context': self.tokenizer.tokenize(after_context)[0]
        }
