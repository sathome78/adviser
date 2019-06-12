# Generated by Django 2.2.1 on 2019-06-11 09:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0004_auto_20190611_0856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analytic',
            name='published_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 11, 9, 18, 48, 564104)),
        ),
        migrations.AlterField(
            model_name='analytic',
            name='short_description',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='analytic',
            name='short_description_en',
            field=models.TextField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='analytic',
            name='short_description_ru',
            field=models.TextField(max_length=500, null=True),
        ),
    ]
