from django.views.generic import FormView, TemplateView

from adviser.forms import ListingForm, SupportForm, REQUEST_CHOICES, AdviserForm
from clients.zendesk_client import ZendeskClient
from clients.pipedrive_client import PipedriveClient


class HomePageView(TemplateView):

    template_name = "main/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView).get_context_data(**kwargs)
        return context


class SupportPageView(FormView):
    template_name = 'main/support.html'
    form_class = SupportForm
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super(SupportPageView, self).get_context_data(**kwargs)
        # context["testing_out"] = "this is a new context var"
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
    template_name = 'main/deal.html'
    form_class = ListingForm
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super(DealPageView, self).get_context_data(**kwargs)
        # context["testing_out"] = "this is a new context var"
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
    template_name = 'main/become_adviser.html'
    form_class = AdviserForm
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super(AdviserFormView, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            PipedriveClient().create_adviser(form.cleaned_data)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class AdviserProfileView(FormView):
    template_name = 'main/adviser_profile.html'
    form_class = AdviserForm
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super(AdviserFormView, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            PipedriveClient().create_adviser(form.cleaned_data)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)