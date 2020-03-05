from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import User



class UpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'photo','birthday')


