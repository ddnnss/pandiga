from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.utils.safestring import mark_safe
from pytils.translit import slugify
from PIL import Image
import uuid
from io import BytesIO
from django.core.files import File
from random import choices
import string
from ckeditor_uploader.fields import RichTextUploadingField
from customuser.models import User
from staticPage.models import City
import os
from django_random_queryset import RandomManager
from pandiga.settings import BASE_DIR

class TechniqueType(models.Model):
    name = models.CharField('Название типа техники', max_length=255, blank=False, null=True)
    image = models.ImageField('Изображение (370 x 130)', upload_to='technique/type/', blank=False, null=True)
    icon = models.ImageField('Иконка для главной (40x45)', upload_to='technique/type/', blank=False, null=True)
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
    old_id = models.IntegerField(blank=True, null=True, editable=False)

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

    def get_icon(self):
        if self.icon:
            return self.icon.url
        else:
            return ''

    def get_absolute_url(self):
        return f'/catalog/{self.name_slug}/'

class TechniqueSection(models.Model):
    type = models.ForeignKey(TechniqueType,blank=False,null=True,on_delete=models.SET_NULL,
                             verbose_name='Относится к типу',related_name='sections')
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
    old_id = models.IntegerField(blank=True, null=True, editable=False)
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
    def get_absolute_url(self):
        return f'/catalog/{self.type.name_slug}/{self.name_slug}/'

class TechniqueSubSection(models.Model):
    section = models.ForeignKey(TechniqueSection,blank=False,null=True,on_delete=models.SET_NULL,
                             verbose_name='Относится к разделу',related_name='subsections')
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
    old_id = models.IntegerField(blank=True, null=True, editable=False)

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

    def get_absolute_url(self):
        return f'/catalog/{self.section.type.name_slug}//{self.section.name_slug}/{self.name_slug}/'

class TechniqueItem(models.Model):
    type = models.ForeignKey(TechniqueType, blank=True, null=True, on_delete=models.SET_NULL,
                                verbose_name='Относится к типу')
    section = models.ForeignKey(TechniqueSection, blank=True, null=True, on_delete=models.SET_NULL,
                                verbose_name='Относится к разделу')
    sub_section = models.ForeignKey(TechniqueSubSection, blank=False, null=True, on_delete=models.SET_NULL,
                                verbose_name='Относится к подразделу')
    owner = models.ForeignKey(User, blank=False, null=True, on_delete=models.SET_NULL,
                                verbose_name='Владелец', related_name='techniques')
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
    rating = models.IntegerField('Рейтинг',default=0)
    rate_times = models.IntegerField('РейтингT',default=0)
    is_moderated = models.BooleanField('Проверена?', default=True)
    is_free = models.BooleanField('Статус свободен?', default=True)
    is_active = models.BooleanField('Учавстует в выдаче?', default=True)
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
        self.section = self.sub_section.section
        self.type = self.sub_section.section.type
        super(TechniqueItem, self).save(*args, **kwargs)

    def get_rating(self):
        try:
            return round(self.rating / self.rate_times)
        except:
            return 0
    def get_absolute_url(self):
        # return f'/catalog/{self.sub_section.section.type.name_slug}/{self.sub_section.section.name_slug}/{self.sub_section.name_slug}/{self.name_slug}'
        return f'/catalog/{self.type.name_slug}/{self.section.name_slug}/{self.sub_section.name_slug}/{self.name_slug}'




    def get_main_image(self):
        return self.images.first().image.url

    def get_rent_type_short(self):
        if self.rent_type == 'day':
            return 'Д'
        else:
            return 'Ч'

    def get_rent_type_long(self):
        if self.rent_type == 'day':
            return 'ДЕНЬ'
        else:
            return 'ЧАС'

    def image_tag(self):
        return mark_safe('<img src="{}" width="100" height="100" />'.format(self.get_main_image()))

    image_tag.short_description = 'Изображение'

    def __str__(self):
        return f'Еденица техники : {self.name}'

    objects = RandomManager()

    class Meta:

        verbose_name = "Техника"
        verbose_name_plural = "Еденицы техники"

class TechniqueItemFavorite(models.Model):
    techniqueitem = models.ForeignKey(TechniqueItem, blank=False, null=True, on_delete=models.CASCADE,
                                      verbose_name='Изображение для')
    user = models.ForeignKey(User, blank=False, null=True, on_delete=models.SET_NULL,
                                verbose_name='Владелец')

    def __str__(self):
        return f'Избранная техника полбзователем  : {self.user.first_name}'

class TechniqueItemImage(models.Model):
    techniqueitem = models.ForeignKey(TechniqueItem, blank=False, null=True, on_delete=models.CASCADE,
                                verbose_name='Изображение для',related_name='images')
    image = models.ImageField('Изображение', upload_to='technique/items/', blank=False, null=True)
    is_moderated = models.BooleanField('Изображение проверено?', default=True)

    def image_tag(self):
        return mark_safe('<img src="{}" width="100" height="100" />'.format(self.image.url))

    image_tag.short_description = 'Изображение'

    def save(self, *args, **kwargs):
        fill_color = '#fff'
        base_image = Image.open(self.image)

        if base_image.mode in ('RGBA', 'LA'):
            background = Image.new(base_image.mode[:-1], base_image.size, fill_color)
            background.paste(base_image, base_image.split()[-1])
            base_image = background
        #os.makedirs('media/items/{}'.format(self.item.id), exist_ok=True)
        watermark = Image.open('static/img/wm.png')
        blob = BytesIO()
        width, height = base_image.size
        transparent = Image.new('RGB', (width, height), (0, 0, 0, 0))
        transparent.paste(base_image, (0, 0))
        transparent.thumbnail((800, 800), Image.ANTIALIAS)
        transparent.paste(watermark, (50, 50), mask=watermark)
       # transparent.show()
        transparent.save(blob, 'JPEG')
        self.image.save(f'{self.techniqueitem.name_slug}.jpg',File(blob), save=False)


        super(TechniqueItemImage, self).save(*args, **kwargs)


class TechniqueItemDoc(models.Model):
    techniqueitem = models.ForeignKey(TechniqueItem, blank=True, null=True, on_delete=models.CASCADE,
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


class SectionSubcribes(models.Model):
    section = models.ForeignKey(TechniqueSection,blank=False,null=True,on_delete=models.CASCADE)
    users = models.ManyToManyField(User)