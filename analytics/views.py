# -*- coding: utf-8 -*-
from django.db.models import F
from django.db.transaction import atomic
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.decorators.gzip import gzip_page
from django.views.generic import TemplateView, ListView
from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination

from analytics.models import Analytic
from analytics.serializers import ArticleSchema

class ArticlePageView(TemplateView):
    template_name = 'main/analitics-detail.html'
    model = Analytic

    def get_object(self, queryset=None):
        return self.model.objects.get(slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        slug = self.kwargs['slug']
        data = super().get_context_data(**kwargs)
        if not slug in self.request.session:
            Analytic.objects.filter(slug=slug).update(views=F("views") + 1)
            self.request.session[slug] = slug
        data['article'] = get_object_or_404(Analytic, slug=slug)


        return data

class ArticlesListPageView(TemplateView):
    template_name = 'main/analitics.html'
    model = Analytic
    queryset = Analytic.objects.filter(published_at__lte=timezone.now(), is_active=True)

    def get(self, request, *args, **kwargs):
        tag = request.GET.get('tag')
        queryset = Analytic.objects.filter(published_at__lte=timezone.now(), is_active=True)

        if tag:
            queryset = queryset.filter(tags__tag_name=tag)
        context = {'articles': queryset.order_by('-published_at')[:6]}
        return render(request, "main/analitics.html", context=context)



class StandardResultsSetPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 100

class ListArticleView(generics.ListAPIView):
    serializer_class = ArticleSchema
    permission_classes = (permissions.AllowAny,)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = Analytic.objects.filter(published_at__lte=timezone.now(), is_active=True)
        tag = self.request.query_params.get('tag')

        if tag:
            queryset = queryset.filter(tags__tag_name=tag)

        return queryset.order_by('-published_at')

