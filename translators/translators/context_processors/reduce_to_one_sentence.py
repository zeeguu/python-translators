from context_processor import ContextProcessor
import nltk.data
from translators.language_codes import code_to_full_language
import os.path

NLTK_DATA_PATH = "~/nltk_data/tokenizers/punkt/%(language)s.pickle"


class ReduceToOneSentence(ContextProcessor):
    # Global storage of tokenizers indexed by language code to prevent reloading of tokenizers
    tokenizers = {

    }

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

        before_context = before_context.strip()
        query = query.strip()
        after_context = after_context.strip()

        # append a bit of whitespace to make sure there is whitespace between query and context
        query = ' ' + query + ' '

        full_sentence = before_context + query + after_context

        # Tokenize sentences
        sentences = self.tokenizer.tokenize(full_sentence)

        print(sentences)

        acc = 0  # accumulator
        sentence_ranges = []

        # Build a list of sentence ranges
        for sentence in sentences:
            sentence_ranges.append((acc, len(sentence) + acc))
            acc += len(sentence)

        # Find the indices of the sentences in which the query occurs
        indices = [idx for idx, sr in enumerate(sentence_ranges)
                   if len(before_context) in range(*sr)
                   or len(before_context + query) in range(*sr)]

        # If the sentence only spans a single sentence
        if len(indices) == 1:
            indices.append(indices[0] + 1)
        else:
            indices[1] += 1

        print(indices)

        # Take the sentences in which the query occurs
        relevant_sentences = sentences[slice(*indices)]

        relevant_full_sentence = ' '.join(relevant_sentences)

        print(sentence_ranges[indices[0] - 1])



if __name__ == '__main__':
    params = {
        'before_context': 'Dit is een zin.                                                                                                                     Dit is nog',
        'query': 'een zin en hier heb je nog een zin. Dat zegt',
        'after_context': 'hij in Back, nadat Brussels '
                         'procureur-generaal Johan Delmulle daar vorig najaar een lans voor had gebroken. '
                         'Daarnaast werkt Geens ook aan een regeling rond spijtoptanten. Een akkoord binnen de '
                         'meerderheid is er nog niet..'
    }


    r = ReduceToOneSentence('nl')
    r.process_context(**params)
