__all__ = ["SpecialFoodCalcForm"]

from django import  forms
from dietcalc.models import Food

class SpecialFoodCalcForm(forms.Form):
    food = forms.ModelChoiceField(label="Специальное питание(аминокислотная смесь)",queryset=Food.objects.filter(deleted=False,special_food=True,is_published=True))
    weight = forms.DecimalField(max_digits=4, decimal_places=1, label="Вес",
                                widget=forms.NumberInput(attrs={'class': 'form-control'}))
    norm_per_kg = forms.DecimalField(label="Норма грамм белка спец.смеси(аминокислотной смеси) на килограмм веса.")


