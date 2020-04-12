from django.db import models

class Tarif(models.Model):
    name = models.CharField('Полное название тарифа', max_length=255, blank=False, null=True)
    short_name = models.CharField('Сокращенное название тарифа', max_length=255, blank=False, null=True)
    price = models.IntegerField('Стоимость', default=0)
    technique_count = models.IntegerField('Размещение техники в любой категории', default=0)
    other_count = models.IntegerField('Размещение техники в категории Строительный инструмент ', default=0)
    new_orders_delay = models.IntegerField('Задержка оповещения о новых заявках', default=0)
    work_section = models.BooleanField('Доступ к разделу Работа',default=False)
    work_notify = models.BooleanField('Получение уведомлений о новых предложениях работы',default=False)
    can_see_phone = models.BooleanField('Возможность видеть нормер телефона', default=False)
    can_call = models.BooleanField('Возможность позвонить Работодателю', default=False)
    can_chat = models.BooleanField('Возможность написать Работодателю', default=False)
    parter_bonus = models.IntegerField('Вознаграждение по партнерской программе %', default=0)
    is_default =  models.BooleanField('Тариф по умолчанию?', default=False)

    def __str__(self):
        return self.name or ''

    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"


