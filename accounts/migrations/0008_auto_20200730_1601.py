# Generated by Django 3.0.6 on 2020-07-30 13:01

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0007_auto_20200730_1417'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserProfile',
            new_name='UserSettings',
        ),
        migrations.AlterModelTable(
            name='usersettings',
            table='user_settings',
        ),
    ]