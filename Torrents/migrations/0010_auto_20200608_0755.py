# Generated by Django 3.0.7 on 2020-06-08 07:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Torrents', '0009_auto_20200608_0754'),
    ]

    operations = [
        migrations.RenameField(
            model_name='likes',
            old_name='post_id',
            new_name='post',
        ),
        migrations.RenameField(
            model_name='likes',
            old_name='user_id',
            new_name='user',
        ),
    ]
