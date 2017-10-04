from flask import Flask, request, Response
import itertools
import math
import json

from python_translators.translators.best_effort_translator import BestEffortTranslator
from python_translators.translators.translator import Translator
from python_translators.translation_query import TranslationQuery
from python_translators.translation_query import TranslationBudget
from python_translators.translation_response import TranslationResponse
app = Flask(__name__)

translators : [Translator] = {}

MAJOR_LANGUAGES = ['en', 'nl']


def setup():
    print('Booting...')
    setup_translators()
    print('Done.')


def setup_translators():
    """
    Loads all the translators ahead of time

    :return:
    """

    for source_language, target_language in itertools.product(MAJOR_LANGUAGES, MAJOR_LANGUAGES):
        if source_language != target_language:
            print(f'Setting up translator for {source_language} -> {target_language}')
            create_translator(source_language, target_language)


def create_translator(source_language: str, target_language: str) -> None:
    translators[(source_language, target_language)] = BestEffortTranslator(source_language, target_language)

setup()


@app.route("/translate", methods=['POST'])
def hello():
    data = request.get_json()

    source_language, target_language = data['source_language'], data['target_language']

    if (source_language, target_language) not in translators:
        create_translator(source_language, target_language)

    query = TranslationQuery(
        before_context=data['before_context'] if 'before_context' in data else '',
        query=data['query'] if 'query' in data else '',
        after_context=data['after_context'] if 'after_context' in data else '',
        max_translations=data['max_translations'] if 'max_translations' in data else 10,
        budget=TranslationBudget(
            money=data['budget']['money'] if ('budget' in data and 'money' in data['budget']) else math.inf,
            time=data['budget']['time'] if ('budget' in data and 'time' in data['budget']) else math.inf
        )
    )

    translator = translators[(source_language, target_language)]

    response = translator.translate(query)

    return Response(response.to_json(), mimetype='text/json')