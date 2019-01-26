# Generated by Django 2.1.4 on 2019-01-25 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='class_num',
            field=models.PositiveSmallIntegerField(choices=[(1, '（1）班'), (2, '（2）班'), (3, '（3）班'), (4, '（4）班'), (5, '（5）班'), (6, '（6）班'), (7, '（7）班'), (8, '（8）班'), (9, '（9）班'), (10, '（10）班'), (11, '（11）班'), (12, '（12）班'), (13, '（13）班'), (14, '（14）班'), (15, '（15）班')]),
        ),
        migrations.AlterField(
            model_name='student',
            name='grade',
            field=models.PositiveSmallIntegerField(choices=[(1, '高一'), (2, '高二'), (3, '高三')]),
        ),
    ]