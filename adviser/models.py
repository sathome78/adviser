import uuid
from audioop import reverse

from django.utils.translation import ugettext_lazy as _
from django.db import models

ADVISER_TYPE_ENUM = (
    (1, 'Company'),
    (2, 'Adviser')
    )

LANGUAGE_TYPE_ENUM = (
    ('en', 'English'),
    ('ru', 'Russian')
    )


class Manager(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    job_title = models.CharField(max_length=255)
    telegram = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
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
    name = models.CharField(max_length=50,
                            help_text="Company name or adviser first name")
    short_description = models.CharField(max_length=300,
                                         help_text="Short description displayed in sidebar")

    is_published = models.BooleanField(default=False)

    telegram = models.CharField(max_length=255, null=True, blank=True)
    linkedin = models.CharField(max_length=255, null=True, blank=True)
    twitter = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)

    member_since = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='images/advisers/', default='images/default-ava.png')

    surname = models.CharField(max_length=255, null=True, blank=True,
                               help_text="Adviser's surname")
    long_description = models.CharField(max_length=700, null=True, blank=True,
                                        help_text="Company's benefits")
    trading_volume = models.IntegerField(null=True, blank=True,
                                         help_text="24h trading volume")
    rating = models.IntegerField(null=True, blank=True,
                                 help_text="Rating CoinMarketCap")

    def __str__(self):
        if self.get_type_display() == "adviser":
            return '{}--{},{}'.format(self.get_type_display(), self.surname, self.name)
        else:
            return '{}--{}'.format(self.get_type_display(), self.surname, self.name)

    class Meta(object):
        verbose_name = _('adviser')
        verbose_name_plural = _('advisers')

    def get_absolute_url(self):
        return reverse("adviser-detail", args=(self.id))