# Generated by Django 2.2.7 on 2020-05-17 05:40

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('technique', '0005_auto_20200516_0920'),
        ('staticPage', '0003_auto_20200516_0920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagetext',
            name='domain',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hometext', to='staticPage.City', verbose_name='Для поддомена'),
        ),
        migrations.CreateModel(
            name='TechniqueTypeText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_h1', models.CharField(blank=True, max_length=255, null=True, verbose_name='Тег H1 (если не указан, выводится название типа) Для вставки города используйте выражение %TOWN%, для склонения города %TOWN_ALIAS%')),
                ('page_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Название страницы SEO')),
                ('page_description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Описание страницы SEO')),
                ('fullText', ckeditor_uploader.fields.RichTextUploadingField(null=True, verbose_name='Текст для страницы типа техники, Для вставки города используйте выражение %TOWN%, для склонения города %TOWN_ALIAS%')),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='staticPage.City', verbose_name='Для поддомена')),
                ('techniqueType', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='technique.TechniqueType', verbose_name='Для типа техники')),
            ],
            options={
                'verbose_name': 'Текст на страницы типа техники',
                'verbose_name_plural': 'Тексты на страниц типа техники',
            },
        ),
        migrations.CreateModel(
            name='SubTechniqueTypeText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_h1', models.CharField(blank=True, max_length=255, null=True, verbose_name='Тег H1 (если не указан, выводится название типа) Для вставки города используйте выражение %TOWN%, для склонения города %TOWN_ALIAS%')),
                ('page_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Название страницы SEO')),
                ('page_description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Описание страницы SEO')),
                ('fullText', ckeditor_uploader.fields.RichTextUploadingField(null=True, verbose_name='Текст для страницы под-типа техники, Для вставки города используйте выражение %TOWN%, для склонения города %TOWN_ALIAS%')),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='staticPage.City', verbose_name='Для поддомена')),
                ('sectionType', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='technique.TechniqueSection', verbose_name='Для под-типа техники')),
            ],
            options={
                'verbose_name': 'Текст на страницы под-типа техники',
                'verbose_name_plural': 'Тексты на страниц под-типа техники',
            },
        ),
        migrations.CreateModel(
            name='SubSectionTechniqueTypeText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_h1', models.CharField(blank=True, max_length=255, null=True, verbose_name='Тег H1 (если не указан, выводится название типа) Для вставки города используйте выражение %TOWN%, для склонения города %TOWN_ALIAS%')),
                ('page_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Название страницы SEO')),
                ('page_description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Описание страницы SEO')),
                ('fullText', ckeditor_uploader.fields.RichTextUploadingField(null=True, verbose_name='Текст для страницы под-под-типа техники техники, Для вставки города используйте выражение %TOWN%, для склонения города %TOWN_ALIAS%')),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='staticPage.City', verbose_name='Для поддомена')),
                ('subSectionType', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='technique.TechniqueSubSection', verbose_name='Для под-под-типа техники')),
            ],
            options={
                'verbose_name': 'Текст на страницы под-под-типа техники техники',
                'verbose_name_plural': 'Тексты на страниц под-под-типа техники техники',
            },
        ),
    ]