from django.db import models
from pytils.translit import slugify
from PIL import Image
import uuid
from random import choices
import string
from ckeditor_uploader.fields import RichTextUploadingField
from customuser.models import User
from staticPage.models import City

class TechniqueType(models.Model):
    name = models.CharField('Название типа техники', max_length=255, blank=False, null=True)
    image = models.ImageField('Изображение (420 x 225)', upload_to='technique/type/', blank=False, null=True)
    name_lower = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    name_slug = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    page_h1 = models.CharField('Тег H1 (если не указан, выводится название типа)',
                               max_length=255, blank=True, null=True)
    page_title = models.CharField('Название страницы SEO', max_length=255, blank=True, null=True)
    page_description = models.CharField('Описание страницы SEO', max_length=255, blank=True, null=True)
    page_keywords = models.TextField('Keywords SEO', blank=True, null=True)
    seo_text = RichTextUploadingField('СЕО текст на страницу', blank=True, null=True)
    views = models.IntegerField('Просмотров категории',blank=True, default=0)
    is_active =models.BooleanField('Отображается на сайте?', default=True)

    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        if not self.name_slug:
            testSlug = TechniqueType.objects.filter(name_slug=slug)
            slugRandom = ''
            if testSlug:
                slugRandom = '-' + ''.join(choices(string.ascii_lowercase + string.digits, k=2))
            self.name_slug = slug + slugRandom
        self.name_lower = self.name.lower()
        super(TechniqueType, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Тип техники"
        verbose_name_plural = "Типы техники"


class TechniqueSection(models.Model):
    type = models.ForeignKey(TechniqueType,blank=False,null=True,on_delete=models.SET_NULL,
                             verbose_name='Относится к типу')
    name = models.CharField('Название раздела техники', max_length=255, blank=False, null=True)
    name_lower = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    name_slug = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    page_h1 = models.CharField('Тег H1 (если не указан, выводится название раздела)', max_length=255,
                               blank=True, null=True)
    page_title = models.CharField('Название страницы SEO', max_length=255, blank=True, null=True)
    page_description = models.CharField('Описание страницы SEO', max_length=255, blank=True, null=True)
    page_keywords = models.TextField('Keywords SEO', blank=True, null=True)
    seo_text = RichTextUploadingField('СЕО текст на страницу', blank=True, null=True)
    views = models.IntegerField('Просмотров категории',blank=True, default=0)
    is_active = models.BooleanField('Отображается на сайте?', default=True)
    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        if not self.name_slug:
            testSlug = TechniqueSection.objects.filter(name_slug=slug)
            slugRandom = ''
            if testSlug:
                slugRandom = '-' + ''.join(choices(string.ascii_lowercase + string.digits, k=2))
            self.name_slug = slug + slugRandom
        self.name_lower = self.name.lower()
        super(TechniqueSection, self).save(*args, **kwargs)

    def __str__(self):
        return f'Раздел техники : {self.name}'

    class Meta:
        verbose_name = "Раздел техники"
        verbose_name_plural = "Разделы техники"


class TechniqueSubSection(models.Model):
    section = models.ForeignKey(TechniqueSection,blank=False,null=True,on_delete=models.SET_NULL,
                             verbose_name='Относится к разделу')
    name = models.CharField('Название подраздела техники', max_length=255, blank=False, null=True)
    name_lower = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    name_slug = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    page_h1 = models.CharField('Тег H1 (если не указан, выводится название подраздела)',
                               max_length=255, blank=True, null=True)
    page_title = models.CharField('Название страницы SEO', max_length=255, blank=True, null=True)
    page_description = models.CharField('Описание страницы SEO', max_length=255, blank=True, null=True)
    page_keywords = models.TextField('Keywords SEO', blank=True, null=True)
    seo_text = RichTextUploadingField('СЕО текст на страницу', blank=True, null=True)
    views = models.IntegerField('Просмотров категории',blank=True, default=0)
    is_active = models.BooleanField('Отображается на сайте?', default=True)

    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        if not self.name_slug:
            testSlug = TechniqueSubSection.objects.filter(name_slug=slug)
            slugRandom = ''
            if testSlug:
                slugRandom = '-' + ''.join(choices(string.ascii_lowercase + string.digits, k=2))
            self.name_slug = slug + slugRandom
        self.name_lower = self.name.lower()
        super(TechniqueSubSection, self).save(*args, **kwargs)

    def __str__(self):
        return f'Раздел техники : {self.name}'

    class Meta:
        verbose_name = "Подраздел техники"
        verbose_name_plural = "Подразделы техники"



class TechniqueItem(models.Model):
    sub_section = models.ForeignKey(TechniqueSubSection, blank=False, null=True, on_delete=models.SET_NULL,
                                verbose_name='Относится к подразделу')
    owner = models.ForeignKey(User, blank=False, null=True, on_delete=models.SET_NULL,
                                verbose_name='Владелец')
    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.SET_NULL,
                                verbose_name='Местоположение')
    name = models.CharField('Название техники', max_length=255, blank=False, null=True)
    name_lower = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    name_slug = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)

    is_moderated = models.BooleanField('Проверена?', default=True)
    is_free = models.BooleanField('Статус свободен?', default=True)
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)

    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        if not self.name_slug:
            testSlug = TechniqueItem.objects.filter(name_slug=slug)
            slugRandom = ''
            if testSlug:
                slugRandom = '-' + ''.join(choices(string.ascii_lowercase + string.digits, k=2))
            self.name_slug = slug + slugRandom
        self.name_lower = self.name.lower()
        super(TechniqueItem, self).save(*args, **kwargs)

    def __str__(self):
        return f'Еденица техники : {self.name}'

    class Meta:
        verbose_name = "Техника"
        verbose_name_plural = "Еденицы техники"


class TechniqueItemImages(models.Model):
    techniqueitem = models.ForeignKey(TechniqueItem, blank=False, null=True, on_delete=models.CASCADE,
                                verbose_name='Изображение для')
    image = models.ImageField('Изображение', upload_to='technique/items/', blank=False, null=True)
    is_moderated = models.BooleanField('Проверена?', default=True)