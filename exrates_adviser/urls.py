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
from django.shortcuts import redirect, render
from django.urls import include, reverse
from django.utils.translation import activate

from adviser.views import (AboutUsPageView, AdviserDemoPageView, AdviserFormView, AdviserProfileView,
                           AdviserUpdateProfileView, AdvisorProfileView, BecomeAdviserPageView, ChatPageView,
                           ClientCenterPageView,
                           DealPageView, FiatPageView, PrivacyPolicyPageView, SupportPageView, TermsPageView)
from analytics.views import ArticlePageView, ArticlesListPageView, ListArticleView

activate('en')

from django.conf import settings
from django.contrib import messages

import requests


def check_recaptcha(function):
    def wrap(request, *args, **kwargs):
        request.recaptcha_is_valid = None
        if request.method == 'POST':
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
                }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            if result['success']:
                request.recaptcha_is_valid = True
            else:
                request.recaptcha_is_valid = False
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def home(request):
    return redirect(reverse("about-us"))


def page_not_found_view(request):
    return render(request, '404.html', {})


urlpatterns = i18n_patterns(
        url(r'^$', home, name='home'),
        url(r'^analytics-detail/(?P<slug>[-\w]+)/$', ArticlePageView.as_view(), name='analytics-detail'),
        url(r'^form-listing/$', check_recaptcha(DealPageView.as_view()), name='deal'),
        url(r'^advisor-demo/$', check_recaptcha(AdviserDemoPageView.as_view()), name='adviser-demo'),

        url(r'^(?P<type>[-\w]+)-profile/(?P<slug>[-\w]+)/$', AdvisorProfileView.as_view(), name='advisor-profile'),

        url(r'^(?P<type>[-\w]+)/(?P<slug>[-\w]+)/update/$', check_recaptcha(AdviserUpdateProfileView.as_view()),
            name='adviser-update'),
        url(r'^(?P<type>[-\w]+)/(?P<slug>[-\w]+)/$', check_recaptcha(AdviserProfileView.as_view()), name='adviser-detail'),

        url(r'^fiat/$', FiatPageView.as_view(), name='fiat'),
        url(r'^client-center/$', ClientCenterPageView.as_view(), name='client-center'),
        url(r'^privacy-policy/$', PrivacyPolicyPageView.as_view(), name='privacy-policy'),
        url(r'^terms-of-use/$', TermsPageView.as_view(), name='terms-of-use'),

        url(r'^become-ambassador/$', BecomeAdviserPageView.as_view(), name='become-advisor'),
        url(r'^about-us/$', check_recaptcha(AboutUsPageView.as_view()), name='about-us'),

        url(r'^ambassador-form/$', AdviserFormView.as_view(), name='advisor-form'),
        url(r'^support-center/$', check_recaptcha(SupportPageView.as_view()), name='support-center'),

        url(r'^chat/$', ChatPageView.as_view(), name='chat'),
        url(r'^analytics/$', ArticlesListPageView.as_view(), name='analytics-list'),



        ) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urls = [url('admin/', admin.site.urls),
url(r'^api/articles/$', ListArticleView.as_view(), name='articles-list1'),
        url('i18n/', include('django.conf.urls.i18n')),
        url(r'^ckeditor/', include('ckeditor_uploader.urls')),
        url(r'^api/', include('api.urls')),
        ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += urls
