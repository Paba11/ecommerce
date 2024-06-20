from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ExtendedUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProductSearchForm(forms.Form):
    search_query = forms.CharField(label='Search', max_length=100)