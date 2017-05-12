
[![Build Status](https://travis-ci.org/mircealungu/python-translators.svg?branch=master)](https://travis-ci.org/mircealungu/python-translators)


# Python translators

This library contains a few wrappers for translation services. As of now it contains two translators: google translator
and glosbe translator. The GlosbeTranslator is a simple translator. It can only translates single words. The GoogleTranslator can also translate phrases and more importantly: words and phrases occurring within other phrases/sentences. We call these context aware translations.

## Installation

1. (Optional) `virtualenv .`
2. `pip install -r requirements`

## Examples

### Dutch to English
Translating "treedt" in the sentence "De directeur treedt af":

```
>>> from translators.google_translator import GoogleTranslator
>>> t = GoogleTranslator(source_language='nl', target_language='en', key='<valid google API key>')

>>> t.ca_translate(before_context='De directeur', query='treedt', after_context='af')
u'resigns'
```

Now a context-less translation:

```
>>> t.translate(query='treedt', source_language='nl', target_language='en')
u'occurs'
```

This is a nonsensical translation whereas the context aware translation is quite accurate.

### English to Dutch

Let's say we want to translate "leaves" in the sentence "He leaves the building". A context-less translation yields

```python
>>> from translators.google_translator import GoogleTranslator
>>> gt = GoogleTranslator(key='<valid api key>', source_language='en', target_language='nl')
>>> gt.translate('leaves')
u'bladeren'
```

It translates to "bladeren" which means leaves as in leaves from a tree.

Adding context gives us the right translation:

```
>>> from translators.google_translator import GoogleTranslator
>>> gt = GoogleTranslator(key='<valid api key>', source_language='en', target_language='nl')
>>> gt.ca_translate(before_context='He', query='leaves', after_context='the building')
'verlaat'
```