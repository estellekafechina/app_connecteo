# Generated by Django 5.1.1 on 2024-10-14 19:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_message_notification_post_comment"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="followers",
            field=models.ManyToManyField(
                blank=True, related_name="following", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
