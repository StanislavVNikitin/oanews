__all__ = ["CreateAndUpdateMyDietForm", "ChangePublicUserDietForm"]

from django import forms

from authapp.models import CustomUser
from dietcalc.models import UserDiet


class CreateAndUpdateMyDietForm(forms.ModelForm):
    name = forms.CharField(label="Название диеты", widget=forms.TextInput(attrs={'class': 'form-control'}))
    age = forms.DecimalField(max_digits=4, decimal_places=1, label="Возрост",
                             widget=forms.NumberInput(attrs={'class': 'form-control'}))
    weight = forms.DecimalField(max_digits=4, decimal_places=1, label="Вес",
                                widget=forms.NumberInput(attrs={'class': 'form-control'}))
    height = forms.IntegerField(label="Рост", widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserDiet
        fields = ['name', 'gender', 'age', 'weight', 'height', 'disease']


class CopyMyDietToUserForm(forms.ModelForm):
    user = forms.ModelChoiceField(label="Пользователь",queryset=CustomUser.objects.filter(is_active=True).order_by('-id'))
    name = forms.CharField(label="Название диеты", widget=forms.TextInput(attrs={'class': 'form-control'}))
    age = forms.DecimalField(max_digits=4, decimal_places=1, label="Возрост",
                             widget=forms.NumberInput(attrs={'class': 'form-control'}))
    weight = forms.DecimalField(max_digits=4, decimal_places=1, label="Вес",
                                widget=forms.NumberInput(attrs={'class': 'form-control'}))
    height = forms.IntegerField(label="Рост", widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserDiet
        fields = ['user', 'name', 'gender', 'age', 'weight', 'height', 'disease']
class ChangePublicUserDietForm(forms.ModelForm):
    is_published = forms.BooleanField(label='Опубликовать', required=False)

    class Meta:
        model = UserDiet
        fields = ['is_published']
