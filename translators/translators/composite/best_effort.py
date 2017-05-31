from translators import GlosbeTranslator
from translators.context_aware_translator import ContextAwareTranslator
from translators.context_processors.remove_unnecessary_sentences import RemoveUnnecessarySentences
from translators.factories.google_translator_factory import GoogleTranslatorFactory


class BestEffortTranslator(ContextAwareTranslator):

    """
        
        Best effort means that here we should try to always prioritize
        giving the best translation to the user. (As opposed to other 
        possible composite translators, like for example, LeastExpensesTranslator).

    
    """

    GOOGLE_CONFIDENCE = 70
    # we'll assume this to be the default value of the google translate
    # this will allow us to rank higher translations that are provided by users we trust
    # this is here, while we think about what is the best place to put it...

    # TODO: In the long term, I expect that the contextual translation to have
    # TODO: a higher likelihood of being correct. However, at the moment it still
    # TODO: returns sometimes the entire phrase and this is broken...
    GOOGLE_CONTEXT_AWARE_CONFIDENCE = 60

    BEST_GLOSBE_CONFIDENCE = 50


    def __init__(self, source_language: str, target_language: str) -> 'BestEffortTranslator':
        super(BestEffortTranslator, self).__init__(source_language, target_language)

        self.source_language = source_language
        self.target_language = target_language

        self.glosbe = GlosbeTranslator(source_language, target_language)
        self.google = GoogleTranslatorFactory.build(source_language, target_language)
        self.add_context_processor(RemoveUnnecessarySentences(source_language))

    def _ca_translate(self, query: str, before_context: str, after_context: str, max_translations: int = 1) -> [str]:
        """
        
            returns a list of possible translations together with their likelihood
            where likelihood is the probability that the translmatin is the correct one.
            
            
        :param query: 
        :param max_translations: 
        :return: [dict(translation=..., likelihood=...)]
        """

        try: 
        	contextual_google_translation = self.google.ca_translate(query, before_context, after_context, 1)[0]
        except Exception as e: 
                print(str(e))
                contextual_google_translation = None

        non_contextual_google = self.google.translate(query, 1)

        translations = [
            dict(
                translation=non_contextual_google,
                likelihood= self.GOOGLE_CONFIDENCE
            )
        ]

        if contextual_google_translation:
            if contextual_google_translation.lower() != non_contextual_google.lower():
                translations.append(
                    dict(
                        translation=contextual_google_translation,
                        likelihood=self.GOOGLE_CONTEXT_AWARE_CONFIDENCE
                    )
                )

        try:
            likelihood = self.BEST_GLOSBE_CONFIDENCE
            for each in self.glosbe.translate(query, max_translations):
                if each.lower() not in [each_dict['translation'].lower() for each_dict in translations]:
                    likelihood -= 1

                    translations.append(
                        dict(
                            translation=each,
                            likelihood=likelihood
                        )
                    )

                    if len(translations) == max_translations:
                        break
        except Exception as e:
            print ("Failed to the the glosbe translations!")
            # The main reason for this try/catch is
            #     https://github.com/mircealungu/python-translators/issues/21

        return translations

    def translate(self, query: str, max_translations: int = 1):
        likelihood = self.GOOGLE_CONFIDENCE
        translations = [
            dict(
                translation=self.google.translate(query, 1),
                likelihood=likelihood)]

        likelihood = self.BEST_GLOSBE_CONFIDENCE
        for each in self.glosbe.translate(query, max_translations - 1):
            likelihood -= 1

            # TODO: Must add Translation class as opposed to working with dicts!!
            translations.append(
                dict(
                    translation=each,
                    likelihood=likelihood
                )
            )

        return translations

