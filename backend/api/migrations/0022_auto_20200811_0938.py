# Generated by Django 2.2.8 on 2020-08-11 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0021_auto_20200810_1613"),
    ]

    operations = [
        migrations.RemoveField(model_name="notification", name="event",),
        migrations.RemoveField(model_name="notification", name="sub_type",),
        migrations.AddField(
            model_name="notification",
            name="type",
            field=models.CharField(
                choices=[
                    ("RECORD__CREATED", "RECORD__CREATED"),
                    ("RECORD__UPDATED", "RECORD__UPDATED"),
                    ("RECORD__DELETED", "RECORD__DELETED"),
                    ("RECORD__RECORD_MESSAGE_ADDED", "RECORD__RECORD_MESSAGE_ADDED"),
                    ("RECORD__RECORD_DOCUMENT_ADDED", "RECORD__RECORD_DOCUMENT_ADDED"),
                    (
                        "RECORD__RECORD_DOCUMENT_MODIFIED",
                        "RECORD__RECORD_DOCUMENT_MODIFIED",
                    ),
                    ("RECORD__CLIENT_MODIFIED", "RECORD__CLIENT_MODIFIED"),
                ],
                default="",
                max_length=75,
            ),
        ),
    ]
