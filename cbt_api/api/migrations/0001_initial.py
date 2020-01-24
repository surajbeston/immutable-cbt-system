# Generated by Django 3.0.2 on 2020-01-24 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Examiner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('exam_id', models.CharField(max_length=100)),
                ('datetime_created', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Examiner_score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField()),
                ('datetime_created', models.DateTimeField(auto_now=True)),
                ('users', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Examiner')),
            ],
        ),
    ]
