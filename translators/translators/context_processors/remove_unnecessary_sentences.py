from .context_processor import ContextProcessor
import nltk.data
from translators.language_codes import code_to_full_language
import os.path

NLTK_DATA_PATH = "~/nltk_data/tokenizers/punkt/%(language)s.pickle"


class RemoveUnnecessarySentences(ContextProcessor):
    # Global storage of tokenizers indexed by language code to prevent reloading of tokenizers
    tokenizers = {}

    def __init__(self, language_code):

        # if a tokenizer was already in our global storage
        if language_code in RemoveUnnecessarySentences.tokenizers:
            self.tokenizer = RemoveUnnecessarySentences.tokenizers[language_code]

        else:
            self.tokenizer = RemoveUnnecessarySentences._load_tokenizer(language_code)
            RemoveUnnecessarySentences.tokenizers[language_code] = self.tokenizer

    @classmethod
    def _load_tokenizer(cls, language_code):
        resource_url = NLTK_DATA_PATH % {'language': code_to_full_language(language_code)}
        resource_url = os.path.expanduser(resource_url)

        tokenizer = nltk.data.load(resource_url)

        return tokenizer

    def process_context(self, before_context, query, after_context):


        # Process before_context
        tokenized_before_context = self.tokenizer.tokenize(before_context)

        if len(tokenized_before_context) > 0:
            before_context = tokenized_before_context[-1]

        # Process after_context
        tokenized_after_context = self.tokenizer.tokenize(after_context)

        if len(tokenized_after_context) > 0:
            after_context = tokenized_after_context[0]

        return {
            'before_context': before_context,
            'query': query,
            'after_context': after_context
        }
