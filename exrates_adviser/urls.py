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
                           BecomeAdviserPageView, AdviserDemoPageView)


def home(request):
    request.session['username'] = request.GET.get('username')
    request.session['email'] = request.GET.get('email')
    request.session['picture'] = request.GET.get('picture')
    return redirect(reverse("about-us"))


def page_not_found_view(request):
    return render(request, '404.html', {})


urlpatterns = [
                  url(r'^$', home, name='home'),

                  url(r'^form-listing/$', DealPageView.as_view(), name='deal'),
                  url(r'^advisor-demo/$', AdviserDemoPageView.as_view(), name='adviser-demo'),

                  url(r'^advisor/(?P<id>[0-9a-f-]+)/update/$', AdviserUpdateProfileView.as_view(),
                      name='adviser-update'),
                  url(r'^advisor/(?P<id>[0-9a-f-]+)/$', AdviserProfileView.as_view(), name='adviser-detail'),

                  url(r'^fiat/$', FiatPageView.as_view(), name='fiat'),
                  url(r'^client-center/$', ClientCenterPageView.as_view(), name='client-center'),
                  url(r'^privacy-policy/$', PrivacyPolicyPageView.as_view(), name='privacy-policy'),
                  url(r'^terms-of-use/$', TermsPageView.as_view(), name='terms-of-use'),

                  url(r'^become-advisor/$', BecomeAdviserPageView.as_view(), name='become-advisor'),
                  url(r'^about-us/$', AboutUsPageView.as_view(), name='about-us'),

                  url(r'^advisor-form/$', AdviserFormView.as_view(), name='advisor-form'),
                  url(r'^support-center/$', SupportPageView.as_view(), name='support-center'),

                  url('admin/', admin.site.urls),
                  url('i18n/', include('django.conf.urls.i18n')),
                  url('api/', include('api.urls')),

                  ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
