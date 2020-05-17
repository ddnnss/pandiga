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
    is_default = models.BooleanField('Домен по умолчанию?',default=False)

    def __str__(self):
        return f'{self.city}'

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города и регионы"


class PageText(models.Model):
    domain = models.ForeignKey(City,blank=True,verbose_name='Для поддомена', null=True, on_delete=models.CASCADE, related_name='hometext')
    indexText = RichTextUploadingField('Текст для главной страницы. Для вставки города используйте выражение %TOWN%, для склонения города %TOWN_ALIAS%', blank=True, null=True)

    def __str__(self):
        return f'Тексты на страницы для города {self.domain.city}'

    class Meta:
        verbose_name = "Текст на страницы"
        verbose_name_plural = "Тексты на страницы"


class TechniqueTypeText(models.Model):
    city = models.ForeignKey(City,blank=False,verbose_name='Для поддомена', null=True, on_delete=models.CASCADE)
    techniqueType = models.ForeignKey('technique.TechniqueType',blank=True,verbose_name='Для типа техники', null=True, on_delete=models.CASCADE)
    page_h1 = models.CharField(
        'Тег H1 (если не указан, выводится название типа) Для вставки города используйте выражение %TOWN%, для склонения города %TOWN_ALIAS%',
        max_length=255, blank=True, null=True)
    page_title = models.CharField('Название страницы SEO', max_length=255, blank=True, null=True)
    page_description = models.CharField('Описание страницы SEO', max_length=255, blank=True, null=True)
    fullText = RichTextUploadingField('Текст для страницы типа техники, Для вставки города используйте выражение %TOWN%, для склонения города %TOWN_ALIAS%', blank=False, null=True)

    def __str__(self):
        return 'Текст на страницы типа техники {} для города {}'.format(self.techniqueType.name, self.city.city)

    class Meta:
        verbose_name = "Текст на страницы типа техники"
        verbose_name_plural = "Тексты на страниц типа техники"

class SubTechniqueTypeText(models.Model):
    city = models.ForeignKey(City,blank=False,verbose_name='Для поддомена', null=True, on_delete=models.CASCADE)
    sectionType = models.ForeignKey('technique.TechniqueSection',blank=True,verbose_name='Для под-типа техники', null=True, on_delete=models.CASCADE)
    page_h1 = models.CharField(
        'Тег H1 (если не указан, выводится название типа) Для вставки города используйте выражение %TOWN%, для склонения города %TOWN_ALIAS%',
        max_length=255, blank=True, null=True)
    page_title = models.CharField('Название страницы SEO', max_length=255, blank=True, null=True)
    page_description = models.CharField('Описание страницы SEO', max_length=255, blank=True, null=True)
    fullText = RichTextUploadingField('Текст для страницы под-типа техники, Для вставки города используйте выражение %TOWN%, для склонения города %TOWN_ALIAS%', blank=False, null=True)

    def __str__(self):
        return 'Текст на страницы под-типа техники {} для города {}'.format(self.sectionType.name, self.city.city)

    class Meta:
        verbose_name = "Текст на страницы под-типа техники"
        verbose_name_plural = "Тексты на страниц под-типа техники"


class SubSectionTechniqueTypeText(models.Model):
    city = models.ForeignKey(City,blank=False,verbose_name='Для поддомена', null=True, on_delete=models.CASCADE)
    subSectionType = models.ForeignKey('technique.TechniqueSubSection',blank=True,verbose_name='Для под-под-типа техники', null=True, on_delete=models.CASCADE)
    page_h1 = models.CharField(
        'Тег H1 (если не указан, выводится название типа) Для вставки города используйте выражение %TOWN%, для склонения города %TOWN_ALIAS%',
        max_length=255, blank=True, null=True)
    page_title = models.CharField('Название страницы SEO', max_length=255, blank=True, null=True)
    page_description = models.CharField('Описание страницы SEO', max_length=255, blank=True, null=True)
    fullText = RichTextUploadingField('Текст для страницы под-под-типа техники техники, Для вставки города используйте выражение %TOWN%, для склонения города %TOWN_ALIAS%', blank=False, null=True)

    def __str__(self):
        return 'Текст на страницы под-под-типа техники техники {} для города {}'.format(self.subSectionType.name, self.city.city)

    class Meta:
        verbose_name = "Текст на страницы под-под-типа техники техники"
        verbose_name_plural = "Тексты на страниц под-под-типа техники техники"