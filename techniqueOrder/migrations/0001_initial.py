# Generated by Django 2.1.4 on 2020-03-09 19:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('technique', '0005_auto_20200309_1704'),
        ('staticPage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TechniqueOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Название')),
                ('name_lower', models.CharField(blank=True, db_index=True, editable=False, max_length=255, null=True)),
                ('name_slug', models.CharField(blank=True, db_index=True, editable=False, max_length=255, null=True)),
                ('rent_time', models.IntegerField(null=True, verbose_name='Время аренды')),
                ('rent_type', models.CharField(blank=True, max_length=10, null=True, verbose_name='Тип аренды по времени')),
                ('order_date', models.DateField(blank=True, null=True, verbose_name='Когда')),
                ('comment', models.TextField(null=True, verbose_name='Описание')),
                ('is_moderated', models.BooleanField(default=True, verbose_name='Проверена?')),
                ('is_active', models.BooleanField(default=True, verbose_name='Учавстует в выдаче?')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='staticPage.City', verbose_name='Местоположение')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customer', to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
                ('section', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='technique.TechniqueSection', verbose_name='Относится к разделу')),
                ('sub_section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='technique.TechniqueSubSection', verbose_name='Относится к подразделу')),
                ('type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='technique.TechniqueType', verbose_name='Относится к типу')),
            ],
        ),
    ]
