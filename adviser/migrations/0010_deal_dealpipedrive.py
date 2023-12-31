# -*- coding: utf-8 -*-# Generated by Django 2.2.1 on 2019-06-23 10:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adviser', '0009_auto_20190623_1010'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_type', models.CharField(choices=[('IEO', 'I need to conduct IEO'), ('Listing', 'I need to list a coin')], max_length=7)),
                ('name', models.CharField(max_length=255)),
                ('telegram', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('company_name', models.CharField(max_length=255)),
                ('link_to_project', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='DealPipeDrive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deal_id', models.IntegerField()),
                ('workspace', models.CharField(max_length=255)),
                ('deal_model_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adviser.Deal')),
            ],
        ),
    ]
