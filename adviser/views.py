# -*- coding: utf-8 -*-
import requests
from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import FormView, TemplateView, UpdateView

from adviser.forms import AdviserForm, AdviserProfileForm, ListingForm, REQUEST_CHOICES, SupportForm
from adviser.models import Adviser, Manager
from clients.pipedrive_client import PipedriveClient
from clients.zendesk_client import ZendeskClient


from functools import wraps

class SupportPageView(FormView):
    template_name = 'main/support-center.html'
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
            request_type = dict(REQUEST_CHOICES)[int(cleaned_data.get('request_type'))]
            email = cleaned_data.get('email')
            message = cleaned_data.get('message')

            ZendeskClient().create_issue(request_type, message, email, files)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_form(self, form_class=None):
        return SupportForm(self.request.POST, self.request.FILES)

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
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class AdviserFormView(FormView):
    template_name = 'adviser/advisor-form.html'
    form_class = AdviserForm
    success_url = '.'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class AdviserUpdateProfileView(UpdateView):
    template_name = 'adviser/adviser_profile.html'
    form_class = AdviserProfileForm
    model = Adviser
    success_url = '.'

    def get_object(self, queryset=None):
        return self.model.objects.get(slug=self.kwargs['slug'])

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class AdviserProfileView(TemplateView):
    template_name = 'adviser/advisor-page.html'
    form_class = AdviserProfileForm
    model = Adviser
    success_url = '.'

    def get_object(self, queryset=None):
        return self.model.objects.get(slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        slug = self.kwargs['slug']
        data = super().get_context_data(**kwargs)
        data['adviser'] = get_object_or_404(Adviser, slug=slug)
        data['username'] = None
        data['form'] = ListingForm
        return data


class FiatPageView(TemplateView):
    template_name = 'main/fiat.html'


class AboutUsPageView(FormView):
    template_name = 'main/about-us.html'

    form_class = ListingForm
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super(AboutUsPageView, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            PipedriveClient().create_deal(form.cleaned_data, [settings.PIPEDRIVE_ME, settings.PIPEDRIVE])
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


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


class BecomeAdviserPageView(TemplateView):
    template_name = 'adviser/become-advisor.html'


class AdviserDemoPageView(TemplateView):
    template_name = 'adviser/adviser_page.html'
    success_url = '.'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['form'] = ListingForm
        return data


class ChatPageView(TemplateView):
    template_name = 'main/support-chat.html'


class AdvisorProfileView(UpdateView):
    template_name = 'adviser/advisor-profile.html'

    form_class = AdviserProfileForm
    model = Adviser
    success_url = '.'

    def get_object(self, queryset=None):
        return self.model.objects.get(slug=self.kwargs['slug'])

    def form_valid(self, form):
        adviser = form.save(commit=False)
        adviser.avatar = form.decode_base64_file(self.request.POST.get("avatar"))
        adviser.save()
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        return super().form_invalid(form)
