import os
import urllib

import requests
import re


def translate(api_key, query, source_language, target_language, before_context='', after_context=''):
    query = "{before_context}<span>{query}</span>{after_context}".format(**locals())

    # Construct URL to send request to
    api_url = build_url(api_key=api_key, query=query,
                        source_language=source_language, target_language=target_language)

    # Send request
    response = requests.get(api_url)

    spanned_translation = response.json()['data']['translations'][0]['translatedText']

    return parse_spanned_string(spanned_translation)


def parse_spanned_string(spanned_string):
    re_opening_tag = re.compile(r"<[\s]*[sS]pan[\s]*>(.*)", flags=re.DOTALL)  # <span> tag

    search_obj = re_opening_tag.search(spanned_string)
    if not search_obj:
        raise Exception('Failed to parse spanned string: no opening span tag found.')

    trail = search_obj.group(1)

    re_closing_tag = re.compile(r"(.*)<[\s]*/[\s]*[sS]pan[\s]*>", flags=re.DOTALL)  # </span> tag

    search_obj = re_closing_tag.search(trail)

    if not search_obj:
        raise Exception('Failed to parse spanned string: no closing tag found.')

    result = search_obj.group(1)

    return result.strip()


def build_url(api_key, query, source_language, target_language):
    """
    :param api_key: a valid Google API key
    :param query:
    :param source_language:
    :param target_language:
    :return:
    """
    API_BASE_URL = 'https://translation.googleapis.com/language/translate/v2?'

    query_params = {
        'key': api_key,
        'target': target_language,
        'source': source_language,
        'q': query,
        'format': 'html'
    }

    encoded_query_params = urllib.urlencode(query_params)

    return API_BASE_URL + encoded_query_params


if __name__ == '__main__':
    print(translate(api_key='AIzaSyACaIwt1PWoXFnp2-b3z3U0FQztNOssohU', query='fietstas', source_language='nl',
                    target_language='en'))
