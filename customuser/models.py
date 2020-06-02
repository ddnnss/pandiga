from .utils import create_random_string
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from staticPage.models import City
from tariff.models import Tarif
from django.core.mail import send_mail
from django.template.loader import render_to_string
import datetime as dt
from datetime import datetime
from django.utils import timezone

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):

    username = None
    tarif = models.ForeignKey(Tarif,blank=True,null=True,on_delete=models.SET_NULL,
                              related_name='Тариф')
    # own_partner_code = models.ForeignKey(ParnterCode,blank=True,null=True,
    #                                      on_delete=models.SET_NULL,
    #                                      related_name='own_partner_code',
    #                                      verbose_name='Персональный портнерский код')
    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.SET_NULL,
                             verbose_name='Местоположение')
    avatar = models.ImageField('Фото', upload_to='user',blank=True,null=True)
    photo = models.CharField('VK аватар', max_length=255, blank=True, null=True)
    first_name = models.CharField('Имя', max_length=50, blank=True, null=True)
    last_name = models.CharField('Фамилия', max_length=50, blank=True, null=True)
    middle_name = models.CharField('Отчество', max_length=50, blank=True, null=True)
    # fullname = models.CharField('Отчество', max_length=50, blank=True, null=True)
    phone = models.CharField('Телефон', max_length=50, blank=True, null=True, unique=True)
    email = models.EmailField('Эл. почта', blank=True, null=True, unique=True)
    birthday = models.DateField('День рождения', blank=True, null=True)
    partner_code = models.CharField('Партнерский код', max_length=100, blank=True, null=True, unique=True)
    balance = models.IntegerField('Баланс', default=0)
    partner_balance = models.IntegerField('Партнерский баланс', default=0)
    rating = models.IntegerField('Рейтинг',default=0)
    tariff_update = models.DateField('Дата начала тарифа', blank=True, null=True)
    tariff_expire = models.DateField('Дата завершения тарифа', blank=True, null=True)
    is_customer = models.BooleanField('Заказчик?', default=False)
    is_blocked = models.BooleanField('Заблокирован?', default=False)
    is_phone_verified = models.BooleanField('Телефон подтвержден?', default=False)
    is_email_verified = models.BooleanField('EMail подтвержден?', default=False)
    verify_code = models.CharField('Код подтверждения', max_length=50, blank=True, null=True)
    notification_id = models.CharField('ID для сообщений', max_length=100, blank=True, null=True, unique=True)
    technique_added = models.IntegerField(default=0)
    rate_times = models.IntegerField(default=0)
    other_added = models.IntegerField(default=0)
    last_activity = models.DateTimeField(auto_now=True)
    old_id = models.IntegerField(blank=True,null=True,editable=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        if self.phone:
            return f'{self.get_full_name()} {self.phone}'
        elif self.email:
            return f'{self.get_full_name()} {self.email}'
        else:
            return f'{self.get_full_name()} {self.id}'

    def get_user_activity(self):
        if (timezone.now() - self.last_activity) > dt.timedelta(seconds=10):
            return f'Был {self.last_activity.strftime("%d.%m.%Y,%H:%M:%S")}'
        else:
            return 'В сети'


    def get_rating(self):
        try:
            return round(self.rating / self.rate_times)
        except:
            return 0
    def get_full_name(self):
        if self.last_name:
            return f'{self.last_name} {self.first_name}'
        else:
            return f'{self.first_name}'

    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        elif self.photo:
            return self.photo
        else:
            return '/static/img/n_a.png'


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True)
    text = models.TextField(blank=True,null=True)
    is_read = models.BooleanField(default=False)
    is_chat_notification = models.BooleanField(default=False)
    is_user_notified = models.BooleanField(default=False)
    redirect_url = models.CharField(max_length=255,blank=True,null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    is_delayed = models.BooleanField(default=False)
    show_time = models.DateTimeField(blank=True, null=True)


def user_post_save(sender, instance, created, **kwargs):
    """Создание всех значений по-умолчанию для нового пользовыателя"""
    if created:
        default_tarif = Tarif.objects.get(is_default=True)
        instance.partner_code = create_random_string(digits=True,num=8)
        instance.tarif = default_tarif
        instance.save()

def notify_post_save(sender, instance, created, **kwargs):
    if created and not instance.is_delayed:
        msg_html = render_to_string('email/notify.html', {'created': instance.createdAt,
                                                            'text': instance.text,
                                                            'url': instance.redirect_url})
        send_mail('Новое оповещение на сайте pandiga.ru', None, 'info@pandiga.ru',
                  [instance.user.email],
                  fail_silently=False, html_message=msg_html)
    elif not instance.is_delayed:
        msg_html = render_to_string('email/notify.html', {'created': instance.createdAt,
                                                          'text': instance.text,
                                                          'url': instance.redirect_url})
        send_mail('Новое оповещение на сайте pandiga.ru', None, 'info@pandiga.ru',
                  [instance.user.email],
                  fail_silently=False, html_message=msg_html)

post_save.connect(user_post_save, sender=User)
post_save.connect(notify_post_save, sender=Notification)