# Generated by Django 5.1.3 on 2024-11-29 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Office_employee",
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
                ("mobile", models.IntegerField()),
                ("pin", models.IntegerField()),
                ("post", models.CharField(max_length=100)),
                ("status", models.IntegerField(default=1)),
            ],
        ),
    ]
