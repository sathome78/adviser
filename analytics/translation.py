# -*- coding: utf-8 -*-
from modeltranslation.translator import translator, TranslationOptions

from adviser.models import Manager, Adviser
from analytics.models import Analytic


class ArticleTranslationOptions(TranslationOptions):
    fields = ('name', 'short_description', 'article')


translator.register(Analytic, ArticleTranslationOptions)