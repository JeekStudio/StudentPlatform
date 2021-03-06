# Generated by Django 2.1.4 on 2019-02-04 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_student_password_changed'),
        ('society', '0007_society_members'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
                ('content', models.TextField(blank=True, null=True)),
                ('place', models.CharField(max_length=32)),
                ('start_time', models.DateTimeField()),
                ('status', models.PositiveSmallIntegerField(choices=[(0, '审核中'), (1, '通过'), (2, '未通过')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='CreditReceivers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveSmallIntegerField()),
                ('semester', models.PositiveSmallIntegerField()),
                ('receivers', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='student.Student')),
            ],
        ),
        migrations.CreateModel(
            name='SocietyTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=8)),
                ('color', models.CharField(max_length=16)),
            ],
        ),
        migrations.AddField(
            model_name='society',
            name='credit',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='creditreceivers',
            name='society',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='society.Society'),
        ),
        migrations.AddField(
            model_name='activityrequest',
            name='society',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='society.Society'),
        ),
        migrations.AddField(
            model_name='society',
            name='tags',
            field=models.ManyToManyField(to='society.SocietyTag'),
        ),
    ]
