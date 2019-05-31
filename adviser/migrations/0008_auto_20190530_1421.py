# Generated by Django 2.2.1 on 2019-05-30 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adviser', '0007_auto_20190530_1109'),
    ]

    operations = [
        migrations.AddField(
            model_name='adviser',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='adviser',
            name='type',
            field=models.IntegerField(choices=[(1, 'Company'), (2, 'Adviser')], default=1, help_text='Account type'),
        ),
    ]
