from django.db import models
from customuser.models import User


class Parnter(models.Model):
    code = models.CharField('Код', max_length=10, blank=True,null=True)

    user = models.ForeignKey(User,blank=False,null=True,
                             on_delete=models.CASCADE,
                             related_name='my_partner',
                             verbose_name='Партнер')
    created_at = models.DateTimeField("Дата использования кода", auto_now_add=True, null=True)
    total_earned = models.IntegerField('Всего начислено', blank=True, null=True, default=0)

    def __str__(self):
        return f'Партнер по коду {self.code}'

    class Meta:
        verbose_name = "Партнер"
        verbose_name_plural = "Партнеры"

class PartnerMoney(models.Model):
    """Начисления партеров"""
    partner = models.ForeignKey(Parnter,blank=False,null=True,
                             on_delete=models.CASCADE,
                             verbose_name='Партнер')
    earned = models.IntegerField('Начислено', blank=True, null=True)
    action = models.CharField('Операция', max_length=10, blank=True,null=True, default=0)
    created_at = models.DateTimeField("Дата начисления", auto_now_add=True)

    def __str__(self):
        return f'Начисление по коду {self.partner.code}'

    class Meta:
        verbose_name = "Начисление"
        verbose_name_plural = "Начисления"