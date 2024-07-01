from django import forms

class AccessKeyForm(forms.Form):
    access_key = forms.CharField(label='Clé de procuration', max_length=100)

class GenerateKeyForm(forms.Form):
    activation_date = forms.DateTimeField(label="Date d'activation", widget=forms.DateInput(attrs={'type': 'date'}))