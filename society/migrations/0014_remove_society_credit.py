# Generated by Django 2.1.7 on 2019-02-14 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('society', '0013_auto_20190212_0805'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='society',
            name='credit',
        ),
    ]
