# -*- coding: utf8 -*-
from unittest import TestCase
from python_translators.translation_query import TranslationQuery
import python_translators.translation_caches.cachekey as caches
import copy


class TestGoogleTranslator(TestCase):
    def setUp(self):
        self.q1 = TranslationQuery(
            before_context="De directeur", query="treedt af", after_context=""
        )

        self.q2 = copy.deepcopy(self.q1)

        self.k1 = caches.CacheKey(
            query=self.q1, source_language="nl", target_language="en"
        )
        self.k2 = caches.CacheKey(
            query=self.q2, source_language="nl", target_language="en"
        )
        self.k3 = caches.CacheKey(
            query=self.q1, source_language="nl", target_language="es"
        )

    def test_equal_to_itself(self):
        self.assertEqual(self.k1, self.k1)

    def test_equal_two_different_objects(self):
        self.assertEqual(self.k1, self.k2)

    def test_equal_queries_but_distinct_languages(self):
        self.assertNotEqual(
            self.k1,
            caches.CacheKey(query=self.q1, source_language="nl", target_language="es"),
        )

    def test_key_is_hashable(self):
        d = {self.k1: "k1", self.k3: "k3"}

        self.assertEqual(
            d[
                caches.CacheKey(
                    query=TranslationQuery(
                        before_context="De directeur",
                        query="treedt af",
                        after_context="",
                    ),
                    source_language="nl",
                    target_language="en",
                )
            ],
            "k1",
        )

        self.assertEqual(
            d[
                caches.CacheKey(
                    query=TranslationQuery(
                        before_context="De directeur",
                        query="treedt af",
                        after_context="",
                    ),
                    source_language="nl",
                    target_language="es",
                )
            ],
            "k3",
        )
