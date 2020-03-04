from django.db import models

class City(models.Model):
    city = models.CharField('Город', max_length=50, blank=True, null=True, db_index=True)
    region = models.CharField('Регион', max_length=100, blank=True, null=True, db_index=True)

    def __str__(self):
        return f'{self.city}'

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города и регионы"