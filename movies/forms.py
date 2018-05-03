from django import forms
from django.utils.translation import gettext_lazy as _


class SearchForm(forms.Form):
    search = forms.TextInput()
    order = forms.TextInput()

    class Meta:
        fields = ('search')
