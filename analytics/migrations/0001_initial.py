# Generated by Django 2.2.1 on 2019-06-11 08:45

import ckeditor_uploader.fields
import datetime
from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Analytic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_type', models.IntegerField(choices=[(1, 'Preview'), (2, 'Article')], default=1)),
                ('name', models.CharField(max_length=255)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from=('name',), unique=True, verbose_name='slug')),
                ('short_description', models.CharField(max_length=500)),
                ('article', ckeditor_uploader.fields.RichTextUploadingField(max_length=2000)),
                ('currency_pair', models.CharField(max_length=100)),
                ('preview_image', models.ImageField(default='images/default-ava.png', upload_to='articles')),
                ('published_at', models.DateTimeField(default=datetime.datetime(2019, 6, 11, 8, 45, 56, 796918))),
                ('is_published', models.BooleanField(default=False)),
                ('facebook_comments', models.BooleanField(default=True)),
                ('facebook_link', models.CharField(blank=True, max_length=255, null=True)),
                ('go_to_trade_link', models.CharField(blank=True, max_length=255, null=True)),
                ('tags', models.ManyToManyField(related_name='article_tags', to='analytics.Tag')),
            ],
            options={
                'verbose_name': 'Analytic article',
                'verbose_name_plural': 'Analytic articles',
            },
        ),
    ]
