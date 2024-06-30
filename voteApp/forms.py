from django import forms

class AccessKeyForm(forms.Form):
    access_key = forms.CharField(label='Enter Access Key', max_length=100)