from context_processor import ContextProcessor
import re


def wordlist_to_regex(words):
    """
    Turns a list of words into a regex that can be searched with. The regex searches for the first occurrence for any
    of the given words.
    
    :param words: a list of words that needs to be searched for
    :return: 
    """
    escaped = map(re.escape, words)
    combined = '|'.join(sorted(escaped, key=len, reverse=True))
    return re.compile(combined)


def find_last_occurrence(substrings, s):
    """
    This function finds the last occurrence of any of the given substrings.
    
    Returns None if none of the words were found
    :param substrings: 
    :param s: 
    :return: 
    """
    substrings = map(lambda w: w[::-1], substrings)  # reverse each word in `substrings`
    s = s[::-1]  # reverse the haystack as well

    regex = wordlist_to_regex(substrings)

    result = regex.search(s)

    if result is None:
        return None

    indices = result.span()
    return len(s) - indices[1], len(s) - indices[0]  # subtract from `len(s)` to account for the reversing


class RemoveUnnecessaryConjunctions(ContextProcessor):
    def __init__(self, conjunctions):
        self.substrings = RemoveUnnecessaryConjunctions._surround_words_with_spaces(conjunctions)

    @staticmethod
    def _surround_words_with_spaces(words):
        return map(lambda w: ' %(w)s ' % {'w': w}, words)

    def _process_before_context(self, before_context):
        """
        Removes unnecessary conjunctions from the `before_context`

        :param before_context: 
        :return: returns the modified `before_context` with unnecessary conjunctions removed from it.
        """

        result = find_last_occurrence(self.substrings, before_context)

        if result is None:  # no conjunctions were found so we return the original `before_context`, unmodified
            return before_context

        return before_context[result[1]:]

    def _process_after_context(self, after_context):
        """
        Removes unnecessary conjunctions from the `after_context`
        
        :param after_context: 
        :return: returns the modified `after_context` with unnecessary conjunctions removed from it.
        """

        r = wordlist_to_regex(self.substrings)

        result = r.search(after_context)

        if result is None:  # no conjunctions were found so we return the original `after_context`, unmodified
            return after_context

        indices = result.span()

        return after_context[:indices[0]]

    def process_context(self, before_context, query, after_context):
        return {
            'before_context': self._process_before_context(before_context),
            'query': query,
            'after_context': self._process_after_context(after_context)
        }
