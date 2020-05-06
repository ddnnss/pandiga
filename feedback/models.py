from django.db import models
from customuser.models import User, Notification
from technique.models import TechniqueItem



class UserFeedback(models.Model):
    from_user = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE,
                                  verbose_name='Отзыв от',related_name='from_user')
    about_user = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE,
                                      verbose_name='Отзыв о',related_name='about_user')
    text = models.TextField('Отзыв', blank=False, null=True)
    rating = models.IntegerField('Оценка', blank=False, null=True)
    createdAt = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        Notification.objects.create(user=self.about_user,
                                    text=f'Пользователь {self.from_user.get_full_name()} оставил о Вас отзыв',
                                    redirect_url='/user/lk/?tab=tab-feedback')
        super(UserFeedback, self).save(*args, **kwargs)

    def __str__(self):
        return f'Отзыв о {self.about_user.first_name} от {self.from_user.first_name} '

class TechniqueFeedback(models.Model):
    from_user = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE,
                                      verbose_name='Отзыв от')
    techniqueitem = models.ForeignKey(TechniqueItem, blank=False, null=True, on_delete=models.CASCADE,
                                      verbose_name='Отзыв о')
    text = models.TextField('Отзыв', blank=False, null=True)
    rating = models.IntegerField('Оценка', blank=False, null=True)
    createdAt = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Отзыв о {self.techniqueitem.name} от {self.from_user.first_name}'

    def save(self, *args, **kwargs):
        Notification.objects.create(user=self.techniqueitem.owner,
                                    text=f'Пользователь {self.from_user.get_full_name()} оставил о Вашей технике',
                                    redirect_url='/user/lk/?tab=tab-feedback')
        super(TechniqueFeedback, self).save(*args, **kwargs)
