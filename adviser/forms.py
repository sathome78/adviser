# -*- coding: utf-8 -*-
from datetime import datetime

from django import forms
from django.conf import settings
from django.forms import ModelForm, model_to_dict
from django.urls import reverse
from django.utils.text import slugify

from adviser.models import Adviser
from clients.pipedrive_client import PipedriveClient

REQUEST_CHOICES = (
    (1, "Funds Withdrawal"),
    (2, "API Issue"),
    (3, "Improvement"),
    (4, "Deposit"),
    (5, "I see issue"),

    (6, "Help with my account"),
    (7, "Trading"),
    (8, "Promotion"),
    (9, "Security"),
    (10, "Business communication"),
    (11, "Application Performance"),
    (12, "Authentication"),
    (13, "Usability"),
    (14, "Other")

    )


class SupportForm(forms.Form):
    request_type = forms.ChoiceField(choices=REQUEST_CHOICES)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea, max_length=700)
    files = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)


LISTING_CHOICES = (
    ("IEO", "I need to conduct IEO"),
    ("Listing", "I need to list a coin")
    )


class ListingForm(forms.Form):
    request_type = forms.ChoiceField(choices=LISTING_CHOICES, widget=forms.RadioSelect)
    name = forms.CharField(max_length=255)
    telegram = forms.CharField(max_length=255, required=False)
    email = forms.EmailField()
    company_name = forms.CharField(max_length=255)
    link_to_project = forms.CharField(max_length=255, required=True)



class AdviserForm(ModelForm):
    name = forms.CharField(max_length=255)
    telegram = forms.CharField(max_length=255)
    email = forms.EmailField()
    linkedin = forms.CharField()

    class Meta:
        model = Adviser
        fields = ['name', 'telegram', 'email', 'linkedin']

    def save(self, commit=True):

        instance = super(AdviserForm, self).save(commit=False)
        instance.type = 1
        if instance:
            model = instance
        else:
            model = self
        edit_url = "{}{}".format(settings.SITE, reverse('adviser-update', kwargs={"slug": slugify(model.name)}))
        update_url = "{}{}".format(settings.SITE, reverse('adviser-detail', kwargs={"slug": slugify(model.name)}))
        PipedriveClient().create_or_update_adviser(model_to_dict(instance), edit_url, update_url, [settings.PIPEDRIVE_ME, settings.PIPEDRIVE])
        if commit:
            instance.save()
        return instance




class AdviserProfileForm(ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Adviser
        fields = ['name',  'short_description', 'email', 'telegram', 'linkedin', 'avatar', ]

    def save(self, commit=True):
        instance = super(AdviserProfileForm, self).save(commit=False)
        instance.member_since = datetime.today()
        if instance:
            model = instance
        else:
            model = self
        edit_url = "{}{}".format(settings.SITE, reverse('adviser-update', kwargs={"slug": slugify(model.name)}))
        update_url = "{}{}".format(settings.SITE, reverse('adviser-detail', kwargs={"slug": slugify(model.name)}))
        PipedriveClient().create_or_update_adviser(model_to_dict(instance), edit_url, update_url, [settings.PIPEDRIVE_ME, settings.PIPEDRIVE])
        if commit:
            instance.save()
        return instance


class AdviserAdminForm(ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Adviser
        fields = ['name', 'short_description', 'email', 'telegram', 'linkedin', 'avatar', ]

    def save(self, commit=True):
        instance = super(AdviserAdminForm, self).save(commit=False)
        if instance:
            model = instance
        else:
            model = self
        edit_url = "{}{}".format(settings.SITE, reverse('adviser-update', kwargs={"slug": slugify(model.name)}))
        update_url = "{}{}".format(settings.SITE, reverse('adviser-detail', kwargs={"slug": slugify(model.name)}))
        PipedriveClient().create_or_update_adviser(model_to_dict(instance), edit_url, update_url, [settings.PIPEDRIVE_ME, settings.PIPEDRIVE])
        if commit:
            instance.save()
        return instance