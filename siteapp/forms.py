from django import forms
from captcha.fields import CaptchaField

class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Емаил', widget=forms.TextInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(label='Тема', widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label='Текст сообщения', widget=forms.Textarea(attrs={'class': 'form-control', "rows": 5}))
    captcha = CaptchaField()