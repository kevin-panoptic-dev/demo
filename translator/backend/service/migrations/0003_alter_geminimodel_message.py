# Generated by Django 5.1.4 on 2024-12-21 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("service", "0002_remove_geminimodel_base_remove_geminimodel_header"),
    ]

    operations = [
        migrations.AlterField(
            model_name="geminimodel",
            name="message",
            field=models.TextField(max_length=500),
        ),
    ]
