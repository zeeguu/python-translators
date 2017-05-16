
[![Build Status](https://travis-ci.org/mircealungu/python-translators.svg?branch=master)](https://travis-ci.org/mircealungu/python-translators)


# Python translators

This library contains a few wrappers for translation services. The GlosbeTranslator is a simple translator. It can only translates single words. The GoogleTranslator can also 
 translate phrases and more importantly: words and phrases occurring within other phrases/sentences. We call these context-aware translations.

## Installation

1. (Optional) `virtualenv .`
2. `pip install -r requirements.txt`
3. `python setup.y install`

## Examples

### Google - Dutch to English
Translating "leer" in the phrase "het stevige leer":

```python
>>> from translators.google_translator import GoogleTranslator
>>> gt = GoogleTranslator(source_language='nl', target_language='en', key='<valid google API key>')

>>> gt.translate('leer')
[u'Learn']
```

Now after adding context:

```python
>>> from translators.google_translator import GoogleTranslator
>>> gt = GoogleTranslator(source_language='nl', target_language='en', key='<valid google API key>')
>>> gt.ca_translate(before_context='het stevige', query='leer', after_context='')
['leather']
```

This is a nonsensical translation whereas the context aware translation is accurate.

### Google - English to Dutch

Let's say we want to translate "leaves" in the sentence "He leaves the building". A context-less translation yields

```python
>>> from translators.google_translator import GoogleTranslator
>>> gt = GoogleTranslator(source_language='en', target_language='nl', key='<valid api key>')
>>> gt.translate('leaves')
[u'bladeren']
```

It translates to "bladeren" which means leaves as in leaves from a tree.

Adding context gives us the right translation:

```python
>>> from translators.google_translator import GoogleTranslator
>>> gt = GoogleTranslator(source_language='en', target_language='nl', key='<valid api key>')
>>> gt.ca_translate(before_context='He', query='leaves', after_context='the building')
['verlaat']
```
