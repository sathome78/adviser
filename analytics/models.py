
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import AutoSlugField

TERM_ENUM = (
    (1, 'Short'),
    (2, 'Long'),
    )

SECTION_ENUM = (
    (1, 'Article'),
    )


class Tag(models.Model):
    tag_name = models.CharField(max_length=100)

    def __str__(self):
        return self.tag_name

class Analytic(models.Model):
    section = models.IntegerField(choices=SECTION_ENUM,
                                default=1)

    title = models.CharField(max_length=255)
    slug = AutoSlugField(_('slug'), max_length=50, unique=True, populate_from=('title',))
    short_description = models.TextField(max_length=500)
    article = RichTextUploadingField(max_length=5000)
    currency_pair = models.CharField(max_length=100)
    term = models.IntegerField(choices=TERM_ENUM,
                                default=1)
    is_active = models.BooleanField(default=True)
    currency_pair_link = models.URLField(max_length=255, null=True, blank=True)
    preview_image = models.ImageField(upload_to='articles', default='images/default-ava.png')

    published_at = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag, related_name='article_tags')
    facebook_comments = models.BooleanField(default=True)
    go_to_trade_link = models.URLField(null=True, blank=True, max_length=255)
    author = models.ForeignKey(User,
                      null=True, blank=True, on_delete=models.SET_NULL)
    views = models.PositiveIntegerField(default=0)

    picture1 = models.ImageField(upload_to='articles/img', null=True, blank=True)
    picture2 = models.ImageField(upload_to='articles/img', null=True, blank=True)
    picture3 = models.ImageField(upload_to='articles/img', null=True, blank=True)


    def __str__(self):
        return self.title

    class Meta(object):
        verbose_name = _('Analytic article')
        verbose_name_plural = _('Analytic articles')

    @property
    def is_published(self):
        return self.published_at <= timezone.now()

    def get_absolute_url(self):
        return reverse("analytics-detail", kwargs={"slug": self.slug})
