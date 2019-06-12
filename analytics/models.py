from datetime import datetime

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django_extensions.db.fields import AutoSlugField

POST_TYPE_ENUM = (
    (1, 'Preview'),
    (2, 'Article'),
    )

class Tag(models.Model):
    tag_name = models.CharField(max_length=100)

    def __str__(self):
        return self.tag_name

class Analytic(models.Model):
    post_type = models.IntegerField(choices=POST_TYPE_ENUM,
                                default=1)
    name = models.CharField(max_length=255)
    slug = AutoSlugField(_('slug'), max_length=50, unique=True, populate_from=('name',))
    short_description = models.TextField(max_length=500)
    article = RichTextUploadingField(max_length=2000)
    currency_pair = models.CharField(max_length=100)
    currency_pair_link = models.CharField(max_length=255, null=True, blank=True)
    preview_image = models.ImageField(upload_to='articles', default='images/default-ava.png')

    published_at = models.DateTimeField(default=datetime.utcnow())
    is_published = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, related_name='article_tags')
    facebook_comments = models.BooleanField(default=True)
    facebook_link = models.CharField(null=True, blank=True, max_length=255)
    go_to_trade_link = models.CharField(null=True, blank=True, max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                      null=True, blank=True, on_delete=models.SET_NULL)
    views = models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.name

    class Meta(object):
        verbose_name = _('Analytic article')
        verbose_name_plural = _('Analytic articles')

    def get_absolute_url(self):
        return reverse("article-detail", kwargs={"slug": self.slug})
