# Generated by Django 2.2.8 on 2020-02-13 23:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("files", "0002_auto_20200212_2009"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="permissionforfolder", name="rlc_has_permission",
        ),
        migrations.RemoveField(
            model_name="permissionforfolder", name="user_has_permission",
        ),
    ]
