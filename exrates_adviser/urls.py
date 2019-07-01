"""exrates_adviser URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect, render, render_to_response
from django.urls import include, reverse

from adviser.views import (SupportPageView, DealPageView, AdviserFormView, AdviserUpdateProfileView, AdviserProfileView,
                           FiatPageView, ClientCenterPageView, PrivacyPolicyPageView, TermsPageView, AboutUsPageView,
                           BecomeAdviserPageView, AdviserDemoPageView, ChatPageView, AdvisorProfileView)
from analytics.views import ArticlePageView, ArticlesListPageView, ListArticleView
from django.utils.translation import activate
activate('en')

def home(request):
    return redirect(reverse("about-us"))


def page_not_found_view(request):
    return render(request, '404.html', {})


urlpatterns = i18n_patterns(
                  url(r'^$', home, name='home'),

                  url(r'^form-listing/$', DealPageView.as_view(), name='deal'),
                  url(r'^ambassador-demo/$', AdviserDemoPageView.as_view(), name='adviser-demo'),

                  url(r'^(?P<type>[-\w]+)/(?P<slug>[-\w]+)/update/$', AdviserUpdateProfileView.as_view(),
                      name='adviser-update'),
                  url(r'^(?P<type>[-\w]+)/(?P<slug>[-\w]+)/$', AdviserProfileView.as_view(), name='adviser-detail'),

                  url(r'^fiat/$', FiatPageView.as_view(), name='fiat'),
                  url(r'^client-center/$', ClientCenterPageView.as_view(), name='client-center'),
                  url(r'^privacy-policy/$', PrivacyPolicyPageView.as_view(), name='privacy-policy'),
                  url(r'^terms-of-use/$', TermsPageView.as_view(), name='terms-of-use'),

                  url(r'^become-ambassador/$', BecomeAdviserPageView.as_view(), name='become-advisor'),
                  url(r'^about-us/$', AboutUsPageView.as_view(), name='about-us'),

                  url(r'^ambassador-form/$', AdviserFormView.as_view(), name='advisor-form'),
                  url(r'^support-center/$', SupportPageView.as_view(), name='support-center'),

                  url(r'^chat/$', ChatPageView.as_view(), name='chat'),
                  url(r'^analytics/$', ArticlesListPageView.as_view(), name='analytics-list'),

                  url(r'^api/articles/$', ListArticleView.as_view(), name='articles-list1'),

                  url(r'^analytics-detail/(?P<slug>[-\w]+)/$', ArticlePageView.as_view(), name='analytics-detail'),

                  url(r'^advisor-profile/$', AdvisorProfileView.as_view(), name='advisor-profile'),



        ) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urls = [url('admin/', admin.site.urls),
                  url('i18n/', include('django.conf.urls.i18n')),
                  url(r'^ckeditor/', include('ckeditor_uploader.urls')),]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += urls
