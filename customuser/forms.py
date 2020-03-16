from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import User



class UpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('avatar','city','email', 'first_name', 'last_name', 'phone', 'photo')


