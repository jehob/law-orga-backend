# Generated by Django 2.2.8 on 2020-09-07 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0027_auto_20200814_1031"),
    ]

    operations = [
        migrations.AlterField(
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
                    ("RECORD__CLIENT_UPDATE", "RECORD__CLIENT_UPDATE"),
                    ("RECORD__NEW_RECORD_PERMISSION", "RECORD__NEW_RECORD_PERMISSION"),
                    ("RECORD__ACCESS_GRANTED", "RECORD__ACCESS_GRANTED"),
                    ("RECORD__ACCESS_DENIED", "RECORD__ACCESS_DENIED"),
                    (
                        "RECORD__DELETION_REQUEST_DENIED",
                        "RECORD__DELETION_REQUEST_DENIED",
                    ),
                    (
                        "RECORD_PERMISSION_REQUEST__REQUESTED",
                        "RECORD_PERMISSION_REQUEST__REQUESTED",
                    ),
                    (
                        "RECORD_PERMISSION_REQUEST__ACCEPTED",
                        "RECORD_PERMISSION_REQUEST__ACCEPTED",
                    ),
                    (
                        "RECORD_PERMISSION_REQUEST__DECLINED",
                        "RECORD_PERMISSION_REQUEST__DECLINED",
                    ),
                    (
                        "RECORD_DELETION_REQUEST__REQUESTED",
                        "RECORD_DELETION_REQUEST__REQUESTED",
                    ),
                    (
                        "RECORD_DELETION_REQUEST__ACCEPTED",
                        "RECORD_DELETION_REQUEST__ACCEPTED",
                    ),
                    (
                        "RECORD_DELETION_REQUEST__DECLINED",
                        "RECORD_DELETION_REQUEST__DECLINED",
                    ),
                    ("USER_REQUEST__REQUESTED", "USER_REQUEST__REQUESTED"),
                    ("USER_REQUEST__ACCEPTED", "USER_REQUEST__ACCEPTED"),
                    ("USER_REQUEST__DECLINED", "USER_REQUEST__DECLINED"),
                    ("GROUP__ADDED_ME", "GROUP__ADDED_ME"),
                    ("GROUP__REMOVED_ME", "GROUP__REMOVED_ME"),
                ],
                default="",
                max_length=75,
            ),
        ),
    ]
