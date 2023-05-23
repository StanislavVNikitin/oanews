__all__ = ["special_food_calc"]

from django.shortcuts import render

from dietcalc.forms import SpecialFoodCalcForm
from dietcalc.models import Food
from siteapp.models import MenuHome


def special_food_calc(request):
    if request.method == 'POST':
        form = SpecialFoodCalcForm(request.POST)
        special_food = Food.objects.get(id=request.POST['food'])
        count_special_food = (100 * (int(request.POST['weight']) * float(request.POST['norm_per_kg'])))/float(special_food.protein)
        return render(request, 'dietcalc/spec_food/calc_view.html', {'form': form, 'menuhome': MenuHome.objects.all(), 'count_special_food': count_special_food, 'special_food_name': special_food})
    else:
        form = SpecialFoodCalcForm()
    return render(request, 'dietcalc/spec_food/calc_view.html', {'form': form,'menuhome': MenuHome.objects.all()})