from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from partner.models import ParnterCode


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
    own_partner_code = models.ForeignKey(ParnterCode,blank=True,null=True,
                                         on_delete=models.SET_NULL,
                                         related_name='own_partner_code',
                                         verbose_name='Персональный портнерский код')
    image = models.ImageField('Фото', upload_to='user',blank=True,null=True)
    first_name = models.CharField('Имя', max_length=50, blank=True, null=True)
    last_name = models.CharField('Фамилия', max_length=50, blank=True, null=True)
    middle_name = models.CharField('Отчество', max_length=50, blank=True, null=True)
    # fullname = models.CharField('Отчество', max_length=50, blank=True, null=True)
    phone = models.CharField('Телефон', max_length=50, blank=True, null=True, unique=True)
    email = models.EmailField('Эл. почта', blank=True, null=True, unique=True)
    birthday = models.DateField('День рождения', blank=True, null=True)
    partner_code = models.CharField('Используемый партнерский код', max_length=100, blank=True, null=True, unique=True)
    balance = models.DecimalField('Баланс',decimal_places=2, max_digits=10, default=0)
    partner_balance = models.DecimalField('Баланс',decimal_places=2, max_digits=10, default=0)
    rating = models.IntegerField('Рейтинг',default=0)
    tariff_update = models.DateField('Дата начала тарифа', blank=True, null=True)
    tariff_expire = models.DateField('Дата завершения тарифа', blank=True, null=True)
    is_customer = models.BooleanField('Заказчик?', default=False)
    is_blocked = models.BooleanField('Заблокирован?', default=False)
    is_phone_verified = models.BooleanField('Телефон подтвержден?', default=False)
    is_email_verified = models.BooleanField('EMail подтвержден?', default=False)
    vkId = models.CharField('vkID', max_length=50, blank=True, null=True)
    fbId = models.CharField('fbID', max_length=50, blank=True, null=True)
    ggId = models.CharField('ggID', max_length=50, blank=True, null=True)
    city = models.CharField('Город', max_length=50, blank=True, null=True)
    verify_code = models.CharField('Код подтверждения', max_length=50, blank=True, null=True)
    sms_verify_code = models.CharField('Код подтверждения для SMS', max_length=50, blank=True, null=True)
    notification_id = models.CharField('ID для сообщений', max_length=100, blank=True, null=True, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

def user_post_save(sender, instance, created, **kwargs):
    """Создание всех значений по-умолчанию для нового пользовыателя"""
    if created:
        new_code = ParnterCode.objects.create(user=instance,code='1234')
        instance.own_partner_code = new_code
        instance.save()

post_save.connect(user_post_save, sender=User)