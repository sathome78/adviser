from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from analytics.models import Analytic, Tag


class AnalyticsAdmin(TabbedTranslationAdmin):

    list_display = ("name",  "post_type", "short_description", "is_published", "published_at")
    list_filter = ('post_type', 'is_published', 'author')
    readonly_fields = ("slug", "author")
    fieldsets = (
        (None, {
            "fields": ("post_type", "name", "slug", "short_description", ),
            }),
        ("Article", {
            "fields": ("article", "preview_image", "published_at", "is_published", "author" ),
            }),
        ("Settings", {
            "fields": ("facebook_comments", "facebook_link", "go_to_trade_link", ),
            }),
        ("Tags", {
            "fields": ("tags", ),
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