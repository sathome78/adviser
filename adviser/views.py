# -*- coding: utf-8 -*-
from django.conf import settings
from django.urls import reverse
from django.utils import translation
from django.views.generic import FormView, TemplateView, UpdateView

from adviser.forms import ListingForm, SupportForm, REQUEST_CHOICES, AdviserForm, AdviserProfileForm
from adviser.models import Adviser, Manager
from clients.zendesk_client import ZendeskClient
from clients.pipedrive_client import PipedriveClient
from django.shortcuts import get_object_or_404, redirect



class SupportPageView(FormView):
    template_name = 'main/support.html'
    form_class = SupportForm
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super(SupportPageView, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('files')
        if form.is_valid():
            cleaned_data = form.cleaned_data
            request_type = dict(REQUEST_CHOICES)[int(cleaned_data.get('request_type') )]
            email = cleaned_data.get('email')
            message = cleaned_data.get('message')

            ZendeskClient().create_issue(request_type, message, email, files)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class DealPageView(FormView):
    template_name = 'main/form-listing.html'
    form_class = ListingForm
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super(DealPageView, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            PipedriveClient().create_deal(form.cleaned_data)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class AdviserFormView(FormView):
    template_name = 'adviser/become_adviser.html'
    form_class = AdviserForm
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super(AdviserFormView, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():

            adviser = form.save()
            edit_url = "{}{}".format(settings.DOMAIN, reverse('adviser-update', kwargs={'id':adviser.id}))
            update_url = "{}{}".format(settings.DOMAIN, reverse('adviser-detail', kwargs={'id': adviser.id}))
            PipedriveClient().create_or_update_adviser(form.cleaned_data, edit_url, update_url)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class AdviserUpdateProfileView(UpdateView):
    template_name = 'adviser/adviser_profile.html'
    form_class = AdviserProfileForm
    model = Adviser
    success_url = '.'

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.kwargs['id'])

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            adviser = form.save()
            edit_url = "{}{}".format(settings.DOMAIN, reverse('adviser-update', kwargs={'id': adviser.id}))
            update_url = "{}{}".format(settings.DOMAIN, reverse('adviser-detail', kwargs={'id': adviser.id}))
            PipedriveClient().create_or_update_adviser(form.cleaned_data, edit_url, update_url)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class AdviserProfileView(TemplateView):
    template_name = 'adviser/advisor-page.html'
    form_class = AdviserProfileForm
    model = Adviser
    success_url = '.'

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.kwargs['id'])

    def get_context_data(self, **kwargs):
        pk = self.kwargs['id']
        data = super().get_context_data(**kwargs)
        data['adviser'] = get_object_or_404(Adviser, pk=pk)
        data['username'] = None
        data['form'] = ListingForm
        return data

class FiatPageView(TemplateView):
    translation.activate('ru')
    template_name = 'main/fiat.html'

class ClientCenterPageView(TemplateView):
    template_name = 'main/client-center.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['contacts'] = Manager.objects.all()
        return data

class PrivacyPolicyPageView(TemplateView):
    template_name = 'main/privacy-policy.html'

class TermsPageView(TemplateView):
    template_name = 'main/terms-of-use.html'