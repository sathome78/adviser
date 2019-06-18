# Generated by Django 2.2.1 on 2019-06-07 16:30

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('adviser', '0003_auto_20190607_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='adviser',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from=('name',), unique=True, verbose_name='slug'),
        ),
    ]
