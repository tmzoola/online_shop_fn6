from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1','password2')

    def clean_password2(self):
        password1 = self.password1
        password2 = self.password2
        if password1 != password2:
            raise forms.ValidationError("Passwords don't match")
