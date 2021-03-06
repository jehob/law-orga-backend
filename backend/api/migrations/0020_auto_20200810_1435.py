# Generated by Django 2.2.8 on 2020-08-10 12:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0019_notification_created"),
    ]

    operations = [
        migrations.RemoveField(model_name="notification", name="user",),
        migrations.CreateModel(
            name="NotificationGroup",
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
                ("last_activity", models.DateTimeField(auto_now_add=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("RECORD", "RECORD"),
                            ("RECORD_PERMISSION_REQUEST", "RECORD_PERMISSION_REQUEST"),
                            ("RECORD_DELETION_REQUEST", "RECORD_DELETION_REQUEST"),
                            ("USER_REQUEST", "USER_REQUEST"),
                            ("GROUP", "GROUP"),
                            ("FILE", "FILE"),
                        ],
                        max_length=100,
                    ),
                ),
                ("read", models.BooleanField(default=False)),
                ("ref_id", models.CharField(max_length=50)),
                ("ref_text", models.CharField(max_length=100, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notification_groups",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
