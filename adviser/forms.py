# -*- coding: utf-8 -*-
from datetime import datetime

from captcha.fields import ReCaptchaField
from django import forms
from django.conf import settings
from django.forms import ModelForm, model_to_dict
from django.urls import reverse
from django.utils.text import slugify

from adviser.models import Adviser, AdviserPipeDrive, Deal, DealPipeDrive, LISTING_CHOICES
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

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
class SupportForm(forms.Form):
    request_type = forms.ChoiceField(choices=REQUEST_CHOICES)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea, max_length=700)
    files = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    captcha = ReCaptchaField(required=True)

class ListingForm(ModelForm):
    request_type = forms.ChoiceField(choices=LISTING_CHOICES, widget=forms.RadioSelect)
    name = forms.CharField(max_length=255)
    telegram = forms.CharField(max_length=255, required=False)
    email = forms.EmailField()
    company_name = forms.CharField(max_length=255)
    link_to_project = forms.CharField(max_length=255, required=True)
    captcha = ReCaptchaField(required=True)

    class Meta:
        model = Deal
        fields = ['request_type', 'name', 'telegram', 'email', 'company_name', 'link_to_project']

    def save(self, commit=True):

        instance = super(ListingForm, self).save(commit=False)
        if instance:
            model = instance
        else:
            model = self
        deals = PipedriveClient().create_deal(model_to_dict(model), [settings.PIPEDRIVE_ME, settings.PIPEDRIVE])

        if commit:
            instance.save()
        for deal in deals:
            adviser_pipedrive = DealPipeDrive(deal_id=deal["deal_id"], deal_model_id=instance.id, workspace=deal["workspace"])
            adviser_pipedrive.save()
        return instance


class AdviserForm(ModelForm):
    name = forms.CharField(max_length=255)
    telegram = forms.CharField(max_length=255)
    email = forms.EmailField()
    linkedin = forms.CharField()
    captcha = ReCaptchaField(required=True)

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
        edit_url = "{}{}".format(settings.SITE, reverse('adviser-update', kwargs={"type": model.get_type_display().lower(), "slug": slugify(model.name)}))
        update_url = "{}{}".format(settings.SITE, reverse('adviser-detail', kwargs={"type": model.get_type_display().lower(), "slug": slugify(model.name)}))
        deals = PipedriveClient().create_or_update_adviser(model_to_dict(instance), edit_url, update_url, [settings.PIPEDRIVE_ME, settings.PIPEDRIVE])

        if commit:
            instance.save()
        for deal in deals:
            adviser_pipedrive = AdviserPipeDrive(deal_id=deal["deal_id"], adviser_id=instance.id, workspace=deal["workspace"])
            adviser_pipedrive.save()
        return instance




class AdviserProfileForm(ModelForm):
    email = forms.EmailField()
    captcha = ReCaptchaField(required=True)

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
        edit_url = "{}{}".format(settings.SITE, reverse('adviser-update', kwargs={"type": model.get_type_display().lower(),"slug": slugify(model.name)}))
        update_url = "{}{}".format(settings.SITE, reverse('adviser-detail', kwargs={"type": model.get_type_display().lower(),"slug": slugify(model.name)}))
        deals = PipedriveClient().create_or_update_adviser(model_to_dict(model), edit_url, update_url,
                                                           [settings.PIPEDRIVE_ME, settings.PIPEDRIVE])
        if commit:
            model.save()
        print(deals)
        for deal in deals:
            adviser_pipedrive = AdviserPipeDrive(deal_id=deal["deal_id"], adviser_id=model.id,
                                                 workspace=deal["workspace"])
            adviser_pipedrive.save()
        return model

    def decode_base64_file(self, data):

        def get_file_extension(file_name, decoded_file):
            import imghdr

            extension = imghdr.what(file_name, decoded_file)
            extension = "jpg" if extension == "jpeg" else extension

            return extension

        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                TypeError('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension,)

            return ContentFile(decoded_file, name=complete_file_name)


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
        edit_url = "{}{}".format(settings.SITE, reverse('adviser-update', kwargs={"type": model.get_type_display().lower(),"slug": slugify(model.name)}))
        update_url = "{}{}".format(settings.SITE, reverse('adviser-detail', kwargs={"type": model.get_type_display(

                ).lower(),"slug": slugify(model.name)}))
        deals = PipedriveClient().create_or_update_adviser(model_to_dict(model), edit_url, update_url,
                                                           [settings.PIPEDRIVE_ME, settings.PIPEDRIVE])
        if commit:
            model.save()
        for deal in deals:
            adviser_pipedrive = AdviserPipeDrive(deal_id=deal["deal_id"], adviser_id=model.id,
                                                 workspace=deal["workspace"])
            adviser_pipedrive.save()
        return model
