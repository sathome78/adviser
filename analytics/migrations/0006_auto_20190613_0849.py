# Generated by Django 2.2.1 on 2019-06-13 08:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0005_auto_20190612_1639'),
    ]

    operations = [
        migrations.AddField(
            model_name='analytic',
            name='currency_pair_link',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='analytic',
            name='published_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
