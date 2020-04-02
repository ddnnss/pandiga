from django.db import models
from technique.models import *
from customuser.models import User
from staticPage.models import City

class TechniqueOrder(models.Model):
    type = models.ForeignKey(TechniqueType, blank=True, null=True, on_delete=models.SET_NULL,
                             verbose_name='Относится к типу')
    section = models.ForeignKey(TechniqueSection, blank=True, null=True, on_delete=models.SET_NULL,
                                verbose_name='Относится к разделу')
    sub_section = models.ForeignKey(TechniqueSubSection, blank=False, null=True, on_delete=models.SET_NULL,
                                    verbose_name='Относится к подразделу')
    customer = models.ForeignKey(User, blank=False, null=True, on_delete=models.SET_NULL,
                              verbose_name='Заказчик', related_name='customer')
    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.SET_NULL,
                             verbose_name='Местоположение')
    worker = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL,
                              verbose_name='Исполнитель', related_name='worker')

    order_apply = models.IntegerField('Выбранная заявка', blank=True,null=True)
    name = models.CharField('Название', max_length=255, blank=False, null=True)
    name_lower = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    name_slug = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    rent_time = models.IntegerField('Время аренды', blank=False, null=True)
    rent_type = models.CharField('Тип аренды по времени', max_length=10, blank=True, null=True)
    order_date = models.DateField('Когда (дата)',blank=True,null=True)
    order_time = models.TimeField('Когда (время)', blank=True, null=True)
    comment = models.TextField('Описание', blank=False, null=True)
    is_moderated = models.BooleanField('Проверена?', default=True)
    is_active = models.BooleanField('Учавстует в выдаче?', default=True)
    is_finished = models.BooleanField('Выполнена?', default=False)
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)

    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        if not self.name_slug:
            testSlug = TechniqueOrder.objects.filter(name_slug=slug)
            slugRandom = ''
            if testSlug:
                slugRandom = '-' + ''.join(choices(string.ascii_lowercase + string.digits, k=2))
            self.name_slug = slug + slugRandom
        self.name_lower = self.name.lower()
        self.section = self.sub_section.section
        self.type = self.sub_section.section.type
        super(TechniqueOrder, self).save(*args, **kwargs)

    def get_absolute_url(self):

        return f'/technique/orders/{self.name_slug}'

    def get_rent_type_short(self):
        if self.rent_type == 'day':
            return 'Д'
        else:
            return 'Ч'

    def get_location(self):
        if self.city:
            return f'{self.city.region}, {self.city.city}'
        else:
            return 'Не указано'

    def __str__(self):
        return f'Заявка на технику № {self.id}, от заказчика {self.customer.first_name}'

    class Meta:
        verbose_name = "Заявка на технику"
        verbose_name_plural = "Заявки на технику"

class TechniqueOrderViewed(models.Model):
    order = models.ForeignKey(TechniqueOrder, blank=True, null=True, on_delete=models.CASCADE,
                             verbose_name='Относится к')
    users = models.ManyToManyField(User, blank=True, verbose_name='Просмотренно пользователями')

    def __str__(self):
        return f'Просмотры заявки №{self.order.id}'

    class Meta:
        verbose_name = "Просмотры заявок"
        verbose_name_plural = "Просмотры заявок"

class TechniqueOrderApply(models.Model):
    order = models.ForeignKey(TechniqueOrder, blank=True, null=True, on_delete=models.CASCADE,
                             verbose_name='Относится к', related_name='applys')
    user = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE,
                      verbose_name='Предложение от')
    technique = models.ForeignKey(TechniqueItem, blank=False, null=True, on_delete=models.CASCADE,
                      verbose_name='Предложенная техника')
    price = models.IntegerField('Предложенная цена', blank=True, null=True)
    is_choosen = models.BooleanField('Заказчик выбрал исполнителя?',blank=True, default=False)
    choose_date = models.DateTimeField("Дата выбора исполнителем", blank=True, null=True)
    is_accepted = models.BooleanField('Предложение принято?',blank=True, null=True)
    accept_date = models.DateTimeField("Дата принятия предложения", blank=True, null=True)
    decline_date = models.DateTimeField("Дата отклонения предложения", blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Отклик на заявку №{self.order.id} от исполнителя {self.user.first_name}'

    class Meta:
        verbose_name = "Отклик на заявку"
        verbose_name_plural = "Отклики на заявки"