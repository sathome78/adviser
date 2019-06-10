# -*- coding: utf-8 -*-
from modeltranslation.translator import translator, TranslationOptions

from adviser.models import Manager, Adviser


class ManagerTranslationOptions(TranslationOptions):
    fields = ('name', 'surname', 'job_title')

class AdviserTranslationOptions(TranslationOptions):
    fields = ('name', 'short_description', 'long_description', 'page_title', 'ambassador_type')

translator.register(Manager, ManagerTranslationOptions)
translator.register(Adviser, AdviserTranslationOptions)