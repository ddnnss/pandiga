# Generated by Django 2.1.4 on 2020-04-07 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customuser', '0004_auto_20200407_1724'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='rate_times',
            field=models.IntegerField(default=0),
        ),
    ]
