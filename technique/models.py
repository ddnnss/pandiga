from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.utils.safestring import mark_safe
from pytils.translit import slugify
from PIL import Image
import uuid
from random import choices
import string
from ckeditor_uploader.fields import RichTextUploadingField
from customuser.models import User
from staticPage.models import City
import os
from pandiga.settings import BASE_DIR

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
    min_rent_time = models.IntegerField('Минимальное время аренды',blank=False,null=True)
    rent_type = models.CharField('Тип аренды по времени', max_length=10, blank=True, null=True)
    rent_price = models.IntegerField('Стоимость аренды',blank=False,null=True)
    description = models.TextField('Описание', blank=False,null=True)
    features = models.TextField('Характеристики', blank=False, null=True)

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

    def get_main_image(self):
        return self.images.first().image.url

    def image_tag(self):
        return mark_safe('<img src="{}" width="100" height="100" />'.format(self.get_main_image()))

    image_tag.short_description = 'Изображение'

    def __str__(self):
        return f'Еденица техники : {self.name}'

    class Meta:
        verbose_name = "Техника"
        verbose_name_plural = "Еденицы техники"


class TechniqueItemImage(models.Model):
    techniqueitem = models.ForeignKey(TechniqueItem, blank=False, null=True, on_delete=models.CASCADE,
                                verbose_name='Изображение для',related_name='images')
    image = models.ImageField('Изображение', upload_to='technique/items/', blank=False, null=True)
    is_moderated = models.BooleanField('Изображение проверено?', default=True)

    def image_tag(self):
        return mark_safe('<img src="{}" width="100" height="100" />'.format(self.image.url))

    image_tag.short_description = 'Изображение'


class TechniqueItemDoc(models.Model):
    techniqueitem = models.ForeignKey(TechniqueItem, blank=False, null=True, on_delete=models.CASCADE,
                                verbose_name='Документ для',related_name='docs')
    image = models.ImageField('Документ', upload_to='technique/docs/', blank=False, null=True)
    is_moderated = models.BooleanField('Документ проверен?', default=True)

    def image_tag(self):
        return mark_safe('<img src="{}" width="100" height="100" />'.format(self.image.url))

    image_tag.short_description = 'Документ'

def auto_delete_image_file_on_delete(sender, instance, **kwargs):
    if instance.image:
        try:
            os.remove(instance.image.path)
        except:
            return False

def auto_delete_image_file_on_change_itemimage(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_file = TechniqueItemImage.objects.get(pk=instance.pk).image
    except TechniqueItemImage.DoesNotExist:
        return False
    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

post_delete.connect(auto_delete_image_file_on_delete, sender=TechniqueItemImage)
pre_save.connect(auto_delete_image_file_on_change_itemimage, sender=TechniqueItemImage)


def auto_delete_doc_file_on_delete(sender, instance, **kwargs):
    if instance.image:
        try:
            os.remove(instance.image.path)
        except:
            return False

def auto_delete_doc_file_on_change_itemimage(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_file = TechniqueItemDoc.objects.get(pk=instance.pk).image
    except TechniqueItemDoc.DoesNotExist:
        return False
    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


post_delete.connect(auto_delete_doc_file_on_delete, sender=TechniqueItemDoc)
pre_save.connect(auto_delete_doc_file_on_change_itemimage, sender=TechniqueItemDoc)