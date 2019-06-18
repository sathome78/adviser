# Generated by Django 2.2.1 on 2019-06-10 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adviser', '0004_adviser_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='adviser',
            name='ambassador_type',
            field=models.CharField(blank=True, default='Verified Ambassador', help_text='Type of ambassador/sales/company', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='adviser',
            name='page_title',
            field=models.CharField(blank=True, default='Ambassador Exrates Exchange', help_text='Title of the page', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='adviser',
            name='type',
            field=models.IntegerField(choices=[(1, 'Company'), (2, 'Ambassador'), (3, 'Sales')], default=1, help_text='Account type'),
        ),
    ]
