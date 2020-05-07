from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class City(models.Model):
    city = models.CharField('Город',
                            max_length=50,
                            blank=True,
                            null=True,
                            db_index=True)
    cityAlias = models.CharField('Склонение города (должно отвечать на вопрос ГДЕ, например, Москве)',
                                 max_length=30,
                                 blank=False,
                                 null=True)
    region = models.CharField('Регион',
                              max_length=100,
                              blank=True,
                              null=True,
                              db_index=True)
    coefficient = models.DecimalField('Коэффициент стоимости размещения',
                                      decimal_places=2,
                                      max_digits=3,
                                      default=1)
    sub_domain = models.CharField('Название поддомена(на пример msk)',
                                  max_length=50,
                                  blank=True,
                                  null=True,
                                  db_index=True)
    title = models.CharField('Тэг Title',
                            max_length=255,
                            blank=True,
                            null=True)
    description = models.CharField('Тэг Description',
                             max_length=255,
                             blank=True,
                             null=True)

    def __str__(self):
        return f'{self.city}'

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города и регионы"


# class PageText(models.Model):
#     domain = models.ForeignKey(City,blank=False,verbose_name='Для поддомена', null=True, on_delete=models.CASCADE, related_name='hometext')
#     indexText = RichTextUploadingField('Текст для главной страницы. Для вставки города используйте выражение %TOWN%, для склонения города %TOWN_ALIAS%', blank=True, null=True)
#
#     def __str__(self):
#         return f'Тексты на страницы для города {self.domain.city}'
#
#     class Meta:
#         verbose_name = "Текст на страницы"
#         verbose_name_plural = "Тексты на страницы"