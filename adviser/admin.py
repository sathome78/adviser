# -*- coding: utf-8 -*-
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TabbedTranslationAdmin

from adviser.forms import AdviserAdminForm
from adviser.models import Adviser, Manager, GeneralFields, AdviserPipeDrive


class AdviserAdmin(TabbedTranslationAdmin):

    list_display = ("id", "type", "name",  "email", "short_description")
    list_filter = ('type', 'member_since')
    readonly_fields = ("id", "slug")
    form = AdviserAdminForm
    actions = ['delete_model']
    fieldsets = (
        (None, {
            "fields": ("id", "type", "name", "slug",  "short_description", "member_since", "avatar"),
            }),
        ("Titles", {
            "fields": ("page_title", "ambassador_type", ),
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

    def delete_model(self, request, obj):
        for adviser in AdviserPipeDrive.objects.filter(adviser_id=obj.id):



    def delete_queryset(self, request, queryset):
        print('========================delete_queryset========================')
        print(queryset)

        """
        you can do anything here BEFORE deleting the object(s)
        """

        queryset.delete()

        """
        you can do anything here AFTER deleting the object(s)
        """

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
