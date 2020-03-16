# Generated by Django 2.1.4 on 2020-03-16 09:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0002_auto_20200316_1225'),
    ]

    operations = [
        migrations.AddField(
            model_name='parnter',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата использования кода'),
        ),
        migrations.AddField(
            model_name='parnter',
            name='total_earned',
            field=models.IntegerField(blank=True, null=True, verbose_name='Всего начислено'),
        ),
        migrations.AlterField(
            model_name='parnter',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='my_partner', to=settings.AUTH_USER_MODEL, verbose_name='Партнер'),
        ),
        migrations.AlterField(
            model_name='partnermoney',
            name='earned',
            field=models.IntegerField(blank=True, null=True, verbose_name='Начислено'),
        ),
    ]