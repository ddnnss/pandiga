# Generated by Django 2.1.4 on 2020-03-09 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_chat_updatedat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='chat',
            name='updatedAt',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
