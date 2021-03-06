# Generated by Django 2.1.4 on 2019-01-25 06:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Society',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('society_id', models.PositiveIntegerField()),
                ('name', models.CharField(max_length=64)),
                ('introduction', models.TextField(blank=True)),
                ('president_name', models.CharField(max_length=64)),
                ('president_class', models.PositiveSmallIntegerField()),
                ('president_grade', models.PositiveSmallIntegerField()),
                ('president_qq', models.CharField(blank=True, max_length=32)),
                ('achievements', models.TextField(blank=True)),
                ('recruit', models.BooleanField(default=False)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('type', models.PositiveSmallIntegerField()),
                ('confirmed', models.BooleanField(default=False)),
                ('recruit_qq_group', models.CharField(blank=True, max_length=32)),
                ('established_time', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SocietyMemberRelationShip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.SmallIntegerField(default=0)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='student.Student')),
                ('society', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='society.Society')),
            ],
        ),
        migrations.AddField(
            model_name='society',
            name='members',
            field=models.ManyToManyField(through='society.SocietyMemberRelationShip', to='student.Student'),
        ),
        migrations.AddField(
            model_name='society',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
