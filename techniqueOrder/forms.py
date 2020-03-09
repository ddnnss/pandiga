from django.forms import ModelForm
from .models import *


class TechniqueOrderForm(ModelForm):
    class Meta:
        model = TechniqueOrder
        fields = ('sub_section',
                  'city',
                  'name',
                  'rent_time',
                  'rent_type',
                  'order_date',
                  'order_time',
                  'comment')


