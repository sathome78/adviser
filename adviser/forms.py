from datetime import datetime

from django import forms
from django.forms import ModelForm

from adviser.models import Adviser

REQUEST_CHOICES = (
    (1, "Funds Withdrawal"),
    (2, "API Issue"),
    (3, "Development sugestions"),
    (4, "Help with Deposit"),
    (5, "Help with withdrawal"),
    (6, "Not receiving email"),
    (7, "Help with clients issue"),
    (8, "Help with google Aut"),
    (9, "Help with SMS Aut"),

    (10, "Help with acoount"),
    (11, "Help with trade"),
    (12, "Prommoutions"),
    (13, "Security issues"),
    (14, "Bussiness comunication"),
    (15, "Service description"),

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
    name = forms.CharField(max_length=255, required=False)
    telegram = forms.CharField(max_length=255, required=False)
    email = forms.EmailField()
    company_name = forms.CharField(max_length=255)
    link_to_project = forms.CharField(max_length=255, required=False)


class AdviserForm(ModelForm):
    name = forms.CharField(max_length=255)
    telegram = forms.CharField(max_length=255, required=False)
    email = forms.EmailField()
    linkedin = forms.CharField(required=False)

    class Meta:
        model = Adviser
        fields = ['name', 'telegram', 'email', 'linkedin']

    def save(self, commit=True):
        instance = super(AdviserForm, self).save(commit=False)
        instance.type = 1
        if commit:
            instance.save()
        return instance


class AdviserProfileForm(ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Adviser
        fields = ['name', 'surname',  'short_description', 'email', 'telegram', 'linkedin', 'avatar', ]

    def save(self, commit=True):
        instance = super(AdviserProfileForm, self).save(commit=False)
        instance.member_since = datetime.today()
        if commit:
            instance.save()
        return instance