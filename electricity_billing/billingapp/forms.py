from django import forms

class alogform(forms.Form):
    username=forms.CharField(max_length=50)
    password=forms.CharField(max_length=50)

class prof(forms.Form):
    img = forms.FileField()
