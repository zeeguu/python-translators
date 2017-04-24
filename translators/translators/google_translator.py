# -*- coding: utf-8 -*-

import os
import re

import HTMLParser
from googleapiclient.discovery import build
from configobj import ConfigObj

from context_aware_translator import ContextAwareTranslator

CONFIG_FILE_PATH = '~/.config/translators.cfg'

re_opening_tag = re.compile(r"<[\s]*[sS]pan[\s]*>(.*)", flags=re.DOTALL)  # <span> tag
re_closing_tag = re.compile(r"(.*?)<[\s]*/[\s]*[sS]pan[\s]*>", flags=re.DOTALL)  # </span> tag


def get_key_from_config():

    if 'TRANSLATE_API_KEY' in os.environ:
        return os.environ['TRANSLATE_API_KEY']

    try:
        config_file = os.path.expanduser(CONFIG_FILE_PATH)
        config = ConfigObj(config_file)
        key = config['TRANSLATE_API_KEY']
        return key
    except KeyError:
        raise Exception('No config file found. Create config file or pass key as argument to constructor')


class GoogleTranslator(ContextAwareTranslator):

    gt_instance = None

    def __init__(self, key=None):

        if not key:
            key = get_key_from_config()

        self.key = key
        self.translation_service = build('translate', 'v2', developerKey=key)

    @classmethod
    def unique_instance(cls, key=None):
        """
            
            The creation of a translator object is slow, since it requires
            sending the secret key and authenticating!  
            
            This is a static class instance that caches a connection and 
            reuses it.
             
        :return: a cached GoogleTranslator object
        """
        if GoogleTranslator.gt_instance:
            return GoogleTranslator.gt_instance

        GoogleTranslator.gt_instance = GoogleTranslator(key)
        return GoogleTranslator.gt_instance

    def translate(self, query, source_language, target_language):
        """
        Translate a query from source language to target language
        :param query:
        :param source_language:
        :param target_language:
        :return:
        """

        params = {
            'source': source_language,
            'target': target_language,
            'q': query,
            'format': 'html'
        }

        translations = self.translation_service.translations().list(**params).execute()

        translation = translations['translations'][0][u'translatedText']

        # Unescape HTML characters
        unescaped_translation = HTMLParser.HTMLParser().unescape(translation)

        print(unescaped_translation)


        return unescaped_translation

    def ca_translate(self, query, source_language, target_language, before_context='', after_context=''):
        """
        Function to translate a query by taking into account the context
        :param query:
        :param source_language:
        :param target_language:
        :param before_context:
        :param after_context:
        :return:
        """
        query = before_context + '<span>' + query + '</span>' + after_context

        translation = self.translate(query, source_language, target_language)

        translated_query = GoogleTranslator.parse_spanned_string(translation).strip()

        stripped_after_context = after_context.strip()

        if stripped_after_context and translated_query and stripped_after_context[0] in ",;'.\"-" \
                and translated_query[-1] == stripped_after_context[0]:
            translated_query = translated_query[:-1]

        return translated_query

    @staticmethod
    def parse_spanned_string(spanned_string):
        search_obj = re_opening_tag.search(spanned_string)

        if not search_obj:
            raise Exception('Failed to parse spanned string: no opening span tag found.')

        trail = search_obj.group(1)
        search_obj = re_closing_tag.search(trail)

        if not search_obj:
            raise Exception('Failed to parse spanned string: no closing tag found.')

        result = search_obj.group(1)

        return result.strip()
