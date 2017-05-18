from django import forms
from phonenumber_field.formfields import PhoneNumberField
from django.forms.models import ModelForm


class UserCreateForm(ModelForm):
    organization = forms.CharField()
    phone_number = PhoneNumberField(label='Phone Number', required=True)
