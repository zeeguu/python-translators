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
>>> from google_translator import GoogleTranslator
>>> t = GoogleTranslator('<valid google API key>')

>>> t.ca_translate(left_context='De directeur', query='treedt', right_context='af', source_language='nl', target_language='en')
u'resigns'
```

Now a context-less translation:

```
>>> t.translate(query='treedt', source_language='nl', target_language='en')
u'occurs'
```

This is a nonsensical translation whereas the context aware translation is quite accurate.

### English to Dutch

Translating (the first occurrence of) "matter" in the sentence "Dark matter is an unidentified type of matter distinct from dark energy."

```
>>> t.ca_translate(left_context='Dark', query='matter', right_context='is an unidentified type of matter distinct from dark energy.', source_language='en', target_language='nl')
u'materie'
```

whereas a context-less translation gives the following result:


```
>>> t.translate(query='matter', source_language='en', target_language='nl')
u'er toe doen'
```

This, again, is nonsensical.