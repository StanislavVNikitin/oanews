__all__ = ["CreateAndUpdateMyFoodForm"]

from django import forms

from dietcalc.models import Food

class CreateAndUpdateMyFoodForm(forms.ModelForm):
    pass

    class Meta:
        model = Food
        fields = ['name', 'protein', 'carbohydrates', 'fat', 'calories', 'special_food', 'category_food']