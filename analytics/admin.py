# -*- coding: utf-8 -*-
from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from analytics.models import Analytic, Tag


class AnalyticsAdmin(TabbedTranslationAdmin):

    list_display = ("title", "short_description", 'is_active', "is_published", "published_at")
    list_filter = ('author', 'tags')
    readonly_fields = ("slug", "author", "views", 'is_published', )
    fieldsets = (
        (None, {
            "fields": ("section",  "title", "term", "currency_pair_link", "currency_pair", "slug", "preview_image","short_description", "published_at",),
            }),
        ("Content", {
            "fields": ("picture1", "picture2", "tags", "article",  "go_to_trade_link", ),
            }),
        ("Settings", {
            "fields": ("facebook_comments",  'is_active', "is_published", "author", "views", ),
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
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(AnalyticsAdmin, self).save_model(request, obj, form, change)


admin.site.register(Analytic, AnalyticsAdmin)
admin.site.register(Tag)