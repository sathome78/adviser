# -*- coding: utf-8 -*-# Generated by Django 2.2.1 on 2019-06-14 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adviser', '0006_auto_20190610_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adviser',
            name='email',
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='adviser',
            name='linkedin',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='adviser',
            name='website',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='manager',
            name='email',
            field=models.EmailField(blank=True, max_length=200, null=True),
        ),
    ]
