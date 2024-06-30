from django import forms

class AccessKeyForm(forms.Form):
    access_key = forms.CharField(label='Enter Access Key', max_length=100)

class GenerateKeyForm(forms.Form):
    activation_date = forms.DateTimeField(label='Activation Date', widget=forms.DateInput(attrs={'type': 'date'}))