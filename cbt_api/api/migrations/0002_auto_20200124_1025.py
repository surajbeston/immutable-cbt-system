# Generated by Django 3.0.2 on 2020-01-24 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examiner',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]