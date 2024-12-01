# Generated by Django 5.1.3 on 2024-11-30 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("office", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Member",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("address", models.CharField(max_length=1000)),
                ("mobile", models.IntegerField()),
                ("pin", models.IntegerField()),
                ("status", models.IntegerField(default=1)),
            ],
        ),
    ]
