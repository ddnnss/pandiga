# Generated by Django 2.1.4 on 2020-04-07 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0004_auto_20200316_1300'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='parnter',
            options={'verbose_name': 'Партнер', 'verbose_name_plural': 'Партнеры'},
        ),
        migrations.AlterModelOptions(
            name='partnermoney',
            options={'verbose_name': 'Начисление', 'verbose_name_plural': 'Начисления'},
        ),
    ]
