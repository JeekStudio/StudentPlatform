# Generated by Django 2.1.4 on 2019-01-26 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_auto_20190125_1204'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='password_changed',
            field=models.BooleanField(default=False),
        ),
    ]
