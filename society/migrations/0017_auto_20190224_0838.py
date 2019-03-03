# Generated by Django 2.1.4 on 2019-02-24 08:38

from django.db import migrations, models
import utils.staticmethods


class Migration(migrations.Migration):

    dependencies = [
        ('society', '0016_society_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='society',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=utils.staticmethods.avatar_storage_path),
        ),
    ]
