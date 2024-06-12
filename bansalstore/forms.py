from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

class RegistrationForm(UserCreationForm):
    email= forms.EmailField(required=True)
    firstname = forms.CharField(required=True)
    class Meta:
        model = User
        fields =['firstname','username','email','password1','password2']
    def save(self,commit=True):
        user = super().save(commit=True)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(label='Username or Email',max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())


