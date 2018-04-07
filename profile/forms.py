from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from profile.models import UserFile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(help_text='Required. Format: yourmail@place.inw')
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        help_text="Your at least 8 digit password can't be entirely numeric",
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}))
    class Meta:
        model = UserFile
        fields = ('file', 'user')
