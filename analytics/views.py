from django.db.models import F
from django.db.transaction import atomic
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView
from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination

from analytics.models import Analytic
from analytics.serializers import ArticleSchema

class ArticleCounterMixin(object):
    def get_context_data(self, **kwargs):
        context = super(ArticleCounterMixin, self).get_context_data(**kwargs)
        article_slug = self.kwargs['slug']
        if not article_slug in self.request.session:
            bp = Analytic.objects.filter(slug=article_slug).update(views=F("views") + 1)
            bp.save()
            # Insert the slug into the session as the user has seen it
            self.request.session[article_slug] = article_slug
        return context

class ArticlePageView(TemplateView, ArticleCounterMixin):
    template_name = 'main/article.html'
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

class ArticlesListPageView(ListView):
    template_name = 'main/articles_list.html'
    model = Analytic
    queryset = Analytic.objects.filter(is_published=True)


    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['articles'] = Analytic.objects.filter(is_published=True)
        return data


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 100

class ListArticleView(generics.ListAPIView):
    serializer_class = ArticleSchema
    permission_classes = (permissions.AllowAny,)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = Analytic.objects.filter(is_published=True)
        tag = self.request.query_params.get('tag')

        if tag:
            queryset = queryset.filter(tags__tag_name=tag)

        return queryset

