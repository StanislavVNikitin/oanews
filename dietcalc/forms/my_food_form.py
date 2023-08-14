__all__ = ["CreateAndUpdateMyFoodForm"]

import decimal
from _decimal import Decimal

from django import forms

from dietcalc.models import Food
from django.core.exceptions import ValidationError

class CreateAndUpdateMyFoodForm(forms.ModelForm):
    def clean(self):
        super().clean()
        errors = {}
        calories = self.cleaned_data['calories']
        calculat_calories = float(self.cleaned_data['protein']) * 4 +  float(self.cleaned_data['carbohydrates']) * 4 + float(self.cleaned_data['fat']) * 9
        diffcalories = float(calories)/calculat_calories
        if (0.98 > diffcalories or diffcalories > 1.02):
            print(diffcalories)
            errors['calories'] = ValidationError(f'Расчетная сумма энергии от БЖУ отличается более 2% и составляет: {round((diffcalories*100)-100,2)}% от вносимой калорийности. Рассчетная из БЖУ:{int(calculat_calories)}Ккал, вводимая: {int(calories)}Ккал')
        if errors:
            raise ValidationError(errors)


    class Meta:
        model = Food
        fields = ['name', 'protein', 'carbohydrates', 'fat', 'calories']


