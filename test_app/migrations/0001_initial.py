from django import VERSION
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone

if VERSION[0] == 2:
    from jsonfield import JSONField
else:
    from django.db.models.fields.json import JSONField


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Person",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name="PersonEvent",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "date",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="Date",
                    ),
                ),
                (
                    "parameters",
                    JSONField(blank=True, default=dict, verbose_name="Parameters"),
                ),
                (
                    "processed",
                    models.BooleanField(default=False, verbose_name="Proccesed"),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("CREATED", "created"),
                            ("UPDATED", "updated"),
                            ("DELETED", "deleted"),
                        ],
                        max_length=128,
                    ),
                ),
                (
                    "person",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="events",
                        to="test_app.Person",
                    ),
                ),
            ],
            options={
                "ordering": ("date",),
                "abstract": False,
            },
        ),
    ]
