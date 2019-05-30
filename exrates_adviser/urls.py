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
from django.conf.urls import url
from django.contrib import admin

from adviser.views import SupportPageView, DealPageView, AdviseFormView

urlpatterns = [

    url(r'^support/$', SupportPageView.as_view(), name='support'),
    url(r'^deal/$', DealPageView.as_view(), name='deal'),
    url(r'^adviser/$', AdviseFormView.as_view(), name='deal'),
    url('admin/', admin.site.urls),
    ]
