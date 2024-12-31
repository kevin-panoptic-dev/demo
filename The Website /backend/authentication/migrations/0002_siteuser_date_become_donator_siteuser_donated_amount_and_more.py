# Generated by Django 5.1.4 on 2024-12-23 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="siteuser",
            name="date_become_donator",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="siteuser",
            name="donated_amount",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="siteuser",
            name="date_joined",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
