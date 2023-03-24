from django import forms
from captcha.fields import CaptchaField
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from siteapp.models import UserStore


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Емаил', widget=forms.TextInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(label='Тема', widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label='Текст сообщения', widget=forms.Textarea(attrs={'class': 'form-control', "rows": 5}))
    captcha = CaptchaField()

class MyUserStoreForm(forms.ModelForm):
    title = forms.CharField(label="Название", widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(widget=CKEditorUploadingWidget, label="Пользовательская история")
    is_published = forms.BooleanField(label='Опубликовать', required = False)

    class Meta:
        model = UserStore
        fields = ['title', 'content', 'is_published']
        widgets = {
            "content": forms.CharField(widget=CKEditorUploadingWidget()),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input form-control', 'role' : 'switch'}),
        }

class ChangePublicUserStoreForm(forms.ModelForm):
    is_published = forms.BooleanField(label='Опубликовать', required = False)

    class Meta:
        model = UserStore
        fields = ['is_published']
