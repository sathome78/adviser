# -*- coding: utf-8 -*-
import re

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import SlugRelatedField

from analytics.models import Analytic, Tag
from exrates_adviser.settings import SITE


class UserSchema(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

class TagSchema(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('tag_name',)

class ArticleSchema(serializers.ModelSerializer):
    author = UserSchema()
    tags = SlugRelatedField(many=True, read_only=True,
        slug_field='tag_name')
    link = SerializerMethodField()
    published_at = SerializerMethodField()
    term = SerializerMethodField()
    views = serializers.IntegerField(read_only=True)

    class Meta:
        model = Analytic
        fields = ('id', 'title', 'slug', 'is_active',
                  'short_description', 'article', 'term', 'currency_pair', 'preview_image', 'published_at', 'is_published', 'facebook_comments',
                  'go_to_trade_link', 'link', 'author', 'tags', 'views', "currency_pair_link")

    def get_link(self, obj):
        return "{}{}".format(SITE, obj.get_absolute_url())

    def get_published_at(self, obj):
        return obj.published_at.strftime("%b/%d/%Y %-I:%-M %p %A")


    def get_term(self, obj):
        return str(obj.get_term_display())