# Generated by Django 5.1.4 on 2024-12-26 02:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("administration", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="extracurricularmodel",
            old_name="date",
            new_name="ext_date",
        ),
    ]