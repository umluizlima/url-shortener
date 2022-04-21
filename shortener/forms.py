from django import forms


class URLCreateForm(forms.Form):
    long_url = forms.URLField(label="URL")
