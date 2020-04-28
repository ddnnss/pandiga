from django.db import models
from customuser.models import User


class PaymentType(models.Model):
    icon = models.ImageField('Иконка', upload_to='payment/', blank=False, null=True)
    name = models.CharField('Название платежа', max_length=255, blank=True, null=True)
    method = models.CharField('Метод платежа', max_length=255, blank=True, null=True)
    is_active = models.BooleanField('Отображать?', default=True)

    def __str__(self):
        return self.name or ''

    class Meta:
        verbose_name = "Вид платежа"
        verbose_name_plural = "Виды платежей"

class PaymentObj(models.Model):
    pay_id = models.CharField('ID платежа',max_length=255,blank=True,null=True)
    user = models.ForeignKey(User, blank=False, null=True,
                                  on_delete=models.CASCADE,
                                  verbose_name='Пользователь')
    type = models.ForeignKey(PaymentType, blank=False, null=True,
                                  on_delete=models.CASCADE,
                                  verbose_name='Вид платежа')
    status = models.CharField('Статус платежа', max_length=255,blank=True,null=True)
    amount = models.IntegerField('Сумма платежа', blank=True,null=True)
    is_payed = models.BooleanField("Оплачен?", default=False)
    created_at = models.DateTimeField("Дата платежа", auto_now_add=True)

    def __str__(self):
        return f'Платеж от {self.created_at}. На сумму {self.amount}. Статус {self.status}'

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"