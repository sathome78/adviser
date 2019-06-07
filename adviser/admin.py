# -*- coding: utf-8 -*-
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TabbedTranslationAdmin

from adviser.forms import AdviserAdminForm
from adviser.models import Adviser, Manager, GeneralFields


class AdviserAdmin(TabbedTranslationAdmin):

    list_display = ("id", "type", "name", "surname", "email", "short_description")
    list_filter = ('type', 'member_since')
    readonly_fields = ("id", )
    form = AdviserAdminForm
    fieldsets = (
        (None, {
            "fields": ("id", "type", "name", "surname",  "short_description", "member_since", "avatar"),
            }),
        ("Contacts", {
            "fields": ("email", "telegram", "linkedin", "twitter", "website",),
            }),
        ("Company params", {
            "description": "Optionally, for company partner only",
            "fields": ("trading_volume", "rating", "long_description",),
            "classes": ("collapse", "collapse-closed"),
            }),
        )

    class Media:
        js = (
            'modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.24/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
            )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
            }

class ManagerAdmin(TabbedTranslationAdmin):

    list_display = ("id", "name", "surname", "job_title",)
    list_display_links = ('name', 'surname')

    fieldsets = (
        (None, {
            "fields": ("name", "surname", "job_title", "avatar"),
            }),
        ("Contacts", {
            "fields": ("telegram", "email",),
            }),
        )

    class Media:
        js = (
            'modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.24/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
            )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
            }



admin.site.register(Adviser, AdviserAdmin)
admin.site.register(Manager, ManagerAdmin)
admin.site.register(GeneralFields)
