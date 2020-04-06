# Generated by Django 2.2.8 on 2020-01-08 14:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20200104_1333'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EncryptionKeys',
            new_name='UserEncryptionKeys',
        ),
        migrations.CreateModel(
            name='UsersRlcKeys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('encrypted_key', models.BinaryField()),
                ('rlc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='encrypted_users_rlc_keys', to='api.Rlc')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_rlc_keys', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RlcEncryptionKeys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_key', models.BinaryField()),
                ('encrypted_private_key', models.BinaryField()),
                ('rlc', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='encryption_keys', to='api.Rlc')),
            ],
        ),
    ]