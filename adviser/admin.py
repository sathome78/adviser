from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from adviser.models import Adviser, Manager


class AdviserAdmin(TranslationAdmin):

    list_display = ("type", "name", "surname", "email", "short_description")
    list_filter = ('type', 'partner_type', 'member_since')

    fieldsets = (
        (None, {
            "fields": ("type", "name", "surname", "partner_type", "short_description", "member_since", "avatar"),
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
            '/static/modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/static/modeltranslation/js/tabbed_translation_fields.js',
            )
        css = {
            'screen': ('/static/modeltranslation/css/tabbed_translation_fields.css',),
            }

class ManagerAdmin(TranslationAdmin):

    list_display = ("name", "surname", "job_title",)

    fieldsets = (
        (None, {
            "fields": ("name", "surname", "job_title"),
            }),
        ("Contacts", {
            "fields": ("telegram", "email",),
            }),
        )
    class Media:
        js = (
            '/static/modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/static/modeltranslation/js/tabbed_translation_fields.js',
            )
        css = {
            'screen': ('/static/modeltranslation/css/tabbed_translation_fields.css',),
            }



admin.site.register(Adviser, AdviserAdmin)
admin.site.register(Manager, ManagerAdmin)
