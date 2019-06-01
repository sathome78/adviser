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
from django.shortcuts import redirect
from django.urls import include, reverse

from adviser.views import (SupportPageView, DealPageView, AdviserFormView, AdviserUpdateProfileView, AdviserProfileView,
                           FiatPageView, ClientCenterPageView, PrivacyPolicyPageView, TermsPageView, AboutUsPageView)


def home(request):
    return redirect(reverse("about-us"))


urlpatterns = i18n_patterns(
        url(r'^$', home, name='home'),

        url(r'^support/$', SupportPageView.as_view(), name='support'),
        url(r'^form-listing/$', DealPageView.as_view(), name='deal'),
        url(r'^adviser/(?P<id>[0-9a-f-]+)/update/$', AdviserUpdateProfileView.as_view(),
            name='adviser-update'),
        url(r'^adviser/(?P<id>[0-9a-f-]+)/$', AdviserProfileView.as_view(), name='adviser-detail'),

        url(r'^fiat/$', FiatPageView.as_view(), name='fiat'),
        url(r'^client-center/$', ClientCenterPageView.as_view(), name='client-center'),
        url(r'^privacy-policy/$', PrivacyPolicyPageView.as_view(), name='privacy-policy'),
        url(r'^terms-of-use/$', TermsPageView.as_view(), name='terms-of-use'),
        url(r'^become-advisor/$', AdviserFormView.as_view(), name='become-advisor'),
        url(r'^about-us/$', AboutUsPageView.as_view(), name='about-us'),

        url(r'^become-advisor-form/$', AdviserFormView.as_view(), name='become-advisor-form'),

        url('admin/', admin.site.urls),
        url('i18n/', include('django.conf.urls.i18n')),

        ) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
