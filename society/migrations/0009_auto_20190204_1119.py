# Generated by Django 2.1.4 on 2019-02-04 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('society', '0008_auto_20190204_1104'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='creditreceivers',
            name='receivers',
        ),
        migrations.RemoveField(
            model_name='creditreceivers',
            name='society',
        ),
        migrations.DeleteModel(
            name='CreditReceivers',
        ),
    ]
