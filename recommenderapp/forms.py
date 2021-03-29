from django import forms
 
class MLForm(forms.Form):
    text = forms.CharField()