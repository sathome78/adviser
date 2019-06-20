# -*- coding: utf-8 -*-
import uuid

from django.conf import settings
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models

from clients.pipedrive_client import PipedriveClient
from django_extensions.db.fields import AutoSlugField

ADVISER_TYPE_ENUM = (
    (1, 'Company'),
    (2, 'Ambassador'),
    (3, 'Sales')
    )


class Manager(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    job_title = models.CharField(max_length=255)
    telegram = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    avatar = models.ImageField(upload_to='images', default='images/default-ava.png')

    def __str__(self):
        return '{}, {}'.format(self.surname, self.name)

    class Meta(object):
        verbose_name = _('sale manager')
        verbose_name_plural = _('sale managers')


class Adviser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.IntegerField(choices=ADVISER_TYPE_ENUM,
                               help_text="Account type", default=1)
    name = models.CharField(max_length=250,
                            help_text="Company name or adviser first name", unique=True)
    short_description = models.CharField(max_length=300,
                                         help_text="Short description displayed in sidebar")

    is_published = models.BooleanField(default=False)

    slug = AutoSlugField(_('slug'), max_length=50, unique=True, populate_from=('name',))

    telegram = models.CharField(max_length=255, null=True, blank=True)
    linkedin = models.URLField(max_length=255, null=True, blank=True)
    twitter = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    website = models.URLField(max_length=255, null=True, blank=True)

    member_since = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='images/advisers/', default='images/default-ava.png')

    long_description = models.CharField(max_length=700, null=True, blank=True,
                                        help_text="Company's benefits")
    trading_volume = models.CharField(max_length=255, null=True, blank=True,
                                      help_text="24h trading volume")
    rating = models.CharField(max_length=255, null=True, blank=True,
                              help_text="Rating CoinMarketCap")

    page_title = models.CharField(max_length=255, null=True, blank=True,
                              help_text="Title of the page", default="Ambassador Exrates Exchange")

    ambassador_type = models.CharField(max_length=255, null=True, blank=True,
                                  help_text="Type of ambassador/sales/company", default="Verified Ambassador")

    deal_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '{}--{}'.format(self.get_type_display(), self.name)

    class Meta(object):
        verbose_name = _('Ambassador')
        verbose_name_plural = _('Ambassadors')

    def get_absolute_url(self):
        return reverse("adviser-detail", kwargs={"slug": self.slug})


class GeneralFields(models.Model):
    telegram_followers = models.CharField(max_length=100)
    twitter_followers = models.CharField(max_length=100)

    facebook_followers = models.CharField(max_length=100)

    trading_volumes = models.CharField(max_length=100)
    active_trades = models.CharField(max_length=100)
    fiat_currencies = models.CharField(max_length=100)
    trading_pairs = models.CharField(max_length=100)

    def __str__(self):
        return 'General fields'

    class Meta(object):
        verbose_name = _('general fields')
        verbose_name_plural = _('general fields')
