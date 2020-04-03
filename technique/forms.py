from django.forms import ModelForm
from .models import *




class AddTechniqueForm(ModelForm):
    class Meta:
        model = TechniqueItem
        fields = ('sub_section',
                  'city',
                  'name',
                  'min_rent_time',
                  'rent_type',
                  'rent_price',
                  'description',
                  'features')


class EditTechniqueForm(ModelForm):
    class Meta:
        model = TechniqueItem
        fields = ('sub_section',
                  'city',
                  'name',
                  'min_rent_time',
                  'rent_type',
                  'rent_price',
                  'description',
                  'features')