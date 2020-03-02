from django.db import models


class ParnterCode(models.Model):
    """Персональный партнерский код"""
    code = models.CharField('Код партнера', max_length=10,blank=True,null=True)
    user = models.ForeignKey('customuser.User',blank=False,null=True,
                             on_delete=models.CASCADE,
                             related_name='user',
                             verbose_name='Код пользователя')
    

class PartnerMoney(models.Model):
    """Начисления партеров"""
    code = models.ForeignKey(ParnterCode,blank=False,null=True,
                             on_delete=models.CASCADE,
                             verbose_name='Код')
    earned = models.DecimalField('Начислено', max_digits=5, decimal_places=2, blank=True, null=True)
    from_user = models.ForeignKey('customuser.User',blank=False,null=True,
                             on_delete=models.CASCADE,
                             related_name='from_user',
                             verbose_name='От пользователя')
    created_at = models.DateTimeField("Дата начисления", auto_now_add=True)