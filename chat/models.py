from django.db import models
from customuser.models import User
from technique.models import TechniqueItem
from techniqueOrder.models import TechniqueOrder

class Chat(models.Model):
    users = models.ManyToManyField(User, blank=True,  verbose_name='Пользователи',
                                    related_name='chatusers')

    techniqueitem = models.ForeignKey(TechniqueItem, blank=True, null=True, on_delete=models.CASCADE,
                                      verbose_name='Тема чата техника')
    order = models.ForeignKey(TechniqueOrder, blank=True, null=True, on_delete=models.CASCADE,
                                      verbose_name='Тема чата заявка')
    isNewMessages = models.BooleanField('Есть новые сообщения', default=False)
    lastMessageOwn = models.BooleanField( default=False)
    lastMsgBy = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE, verbose_name='Сообщение от')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class Message(models.Model):
    chat = models.ForeignKey(Chat, blank=False, null=True, on_delete=models.CASCADE, verbose_name='В чате')
    user = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE, verbose_name='Сообщение от')
    message = models.TextField('Сообщение', blank=True,null=True)
    isUnread = models.BooleanField('Не прочитанное сообщение', default=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.isUnread:
            self.chat.isNewMessages = True
            self.chat.save()
        super(Message, self).save(*args, **kwargs)
