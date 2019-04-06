from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class StaffForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label='Hasło')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Powtórzone hasło')

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', ]
        help_texts = {
            'username': '',
        }

    def clean(self):
        password1 = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise ValidationError('Hasła są różne')
        return self.cleaned_data
