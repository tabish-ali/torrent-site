# Generated by Django 3.0.7 on 2020-06-08 07:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Torrents', '0006_auto_20200607_1345'),
    ]

    operations = [
        migrations.RenameField(
            model_name='uploadtorrents',
            old_name='likes',
            new_name='total_likes',
        ),
        migrations.RenameField(
            model_name='uploadtorrents',
            old_name='unlikes',
            new_name='total_unlikes',
        ),
        migrations.AlterField(
            model_name='likes',
            name='post_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Torrents.UploadTorrents'),
        ),
        migrations.AlterField(
            model_name='likes',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
