# Generated by Django 2.2.1 on 2019-05-28 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adviser', '0003_auto_20190528_1506'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='adviser',
            options={'verbose_name': 'adviser', 'verbose_name_plural': 'advisers'},
        ),
        migrations.AddField(
            model_name='manager',
            name='job_title',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
    ]
