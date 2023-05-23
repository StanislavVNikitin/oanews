__all__ = ["SpecialFoodCalcForm"]

from django import  forms
from dietcalc.models import Food

class SpecialFoodCalcForm(forms.Form):
    food = forms.ModelChoiceField(label="Специальное питание(аминокислотной смеси)",queryset=Food.objects.filter(deleted=False,special_food=True,is_published=True))
    weight = forms.IntegerField(label="Вес пациента в килограмах")
    norm_per_kg = forms.DecimalField(label="Норма грамм белка спец.смести(аминокислотной смеси) на килогорамм веса.")


