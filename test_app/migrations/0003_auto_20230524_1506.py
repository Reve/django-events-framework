# Generated by Django 3.2 on 2023-05-24 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0002_auto_20220208_1247'),
    ]

    operations = [
        migrations.AddField(
            model_name='personevent',
            name='error',
            field=models.BooleanField(default=False, verbose_name='Has error?'),
        ),
        migrations.AddField(
            model_name='personevent',
            name='error_message',
            field=models.TextField(default=None, verbose_name='Error message'),
            preserve_default=False,
        ),
    ]
