# Generated by Django 2.1.4 on 2019-02-12 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('society', '0012_auto_20190211_1631'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='society',
            name='confirmed',
        ),
        migrations.AddField(
            model_name='society',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, '审核中'), (1, '活跃'), (2, '归档')], default=0),
        ),
    ]
