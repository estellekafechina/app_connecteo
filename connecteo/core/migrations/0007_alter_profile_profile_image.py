# Generated by Django 5.1.1 on 2024-10-24 17:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0006_profile_confirmation_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="profile_image",
            field=models.ImageField(blank=True, null=True, upload_to="profiles/"),
        ),
    ]
