# Generated by Django 2.1.4 on 2020-03-16 07:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isNewMessages', models.BooleanField(default=False, verbose_name='Есть новые сообщения')),
                ('lastMessageOwn', models.BooleanField(default=False)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True, null=True, verbose_name='Сообщение')),
                ('isUnread', models.BooleanField(default=True, verbose_name='Не прочитанное сообщение')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('chat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='chat.Chat', verbose_name='В чате')),
            ],
        ),
    ]