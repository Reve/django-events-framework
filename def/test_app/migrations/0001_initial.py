# Generated by Django 3.2 on 2021-12-20 10:57

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='TestEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date')),
                ('parameters', models.JSONField(blank=True, default=dict, verbose_name='Parameters')),
                ('processed', models.BooleanField(default=False, verbose_name='Proccesed')),
                ('type', models.CharField(choices=[('CREATED', 'created'), ('UPDATED', 'updated'), ('DELETED', 'deleted')], max_length=128)),
                ('test_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='test_app.testobject')),
            ],
            options={
                'ordering': ('date',),
                'abstract': False,
            },
        ),
    ]
