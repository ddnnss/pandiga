# Generated by Django 2.2.7 on 2020-05-07 10:18

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('technique', '0003_auto_20200507_0930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='techniqueitem',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='techniqueitem',
            name='features',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True, verbose_name='Характеристики'),
        ),
        migrations.AlterField(
            model_name='techniqueitemfavorite',
            name='techniqueitem',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='technique.TechniqueItem', verbose_name='Техника'),
        ),
        migrations.AlterField(
            model_name='techniqueitemfavorite',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.CreateModel(
            name='TechniqueItemHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summ', models.IntegerField(default=0, verbose_name='Сумма')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('techniqueitem', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='technique.TechniqueItem', verbose_name='Техника')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'История списание за технику',
                'verbose_name_plural': 'История списание за технику',
            },
        ),
    ]