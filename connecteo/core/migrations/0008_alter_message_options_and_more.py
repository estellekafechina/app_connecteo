# Generated by Django 5.1.1 on 2024-10-24 17:40

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0007_alter_profile_profile_image"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="message",
            options={"ordering": ["timestamp"]},
        ),
        migrations.RenameField(
            model_name="message",
            old_name="recipient",
            new_name="receiver",
        ),
    ]
