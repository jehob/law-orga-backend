# Generated by Django 2.2.8 on 2020-09-07 06:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("recordmanagement", "0019_auto_20200827_0916"),
    ]

    operations = [
        migrations.AddField(
            model_name="encryptedrecorddocumentdeletionrequest",
            name="record",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="document_deletions_requests",
                to="recordmanagement.EncryptedRecord",
            ),
        ),
    ]
