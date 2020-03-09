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
                              verbose_name='Владелец', related_name='customer')
    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.SET_NULL,
                             verbose_name='Местоположение')
    name = models.CharField('Название', max_length=255, blank=False, null=True)
    name_lower = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    name_slug = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    rent_time = models.IntegerField('Время аренды', blank=False, null=True)
    rent_type = models.CharField('Тип аренды по времени', max_length=10, blank=True, null=True)
    order_date = models.DateField('Когда (дата)',blank=True,null=True)
    order_time = models.DateField('Когда (время)', blank=True, null=True)
    comment = models.TextField('Описание', blank=False, null=True)
    is_moderated = models.BooleanField('Проверена?', default=True)
    is_active = models.BooleanField('Учавстует в выдаче?', default=True)
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
