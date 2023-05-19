__all__ = ["add_food_to_diet"]

from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from dietcalc.models import Food, UserDiet, Diet

@login_required()
def add_food_to_diet(request):
    if request.method == 'POST':
        if request.POST['food_id'] and request.POST['food_count'] and request.POST['userdiet']:
            itemdiet, created = Diet.objects.update_or_create(
                user_diet=UserDiet.objects.get(id=request.POST['userdiet']),
                food=Food.objects.get(id=request.POST['food_id']),
                defaults={'count': 0},
            )
            itemdiet.count = request.POST['food_count']
            itemdiet.save()
        else:
            print('не полные данные')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect("dietcalc:mydiets")