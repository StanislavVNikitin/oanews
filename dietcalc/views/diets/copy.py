__all__ = ["copy_my_diet", "copy_my_diet_to_user"]

import string
import random

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from pytils.translit import slugify

from dietcalc.forms.my_diet_form import CopyMyDietToUserForm
from siteapp.models import MenuHome
from dietcalc.forms import CreateAndUpdateMyDietForm

from dietcalc.models import UserDiet, Diet


def copy_my_diet(request, pk):
    if request.method == 'POST':
        if UserDiet.objects.get(pk=pk).user == request.user:
            form = CreateAndUpdateMyDietForm(request.POST)
            if form.is_valid():
                new_slug_userdiet = slugify(form.cleaned_data['name'])[:90] + '-' + ''.join(
                    random.choices(string.ascii_uppercase + string.ascii_lowercase, k=12))
                data_user_diet = {**form.cleaned_data, **{'user_id': request.user.id, 'slug': new_slug_userdiet}}
                new_user_diet = UserDiet.objects.create(**data_user_diet)
                contains_food_in_diet = Diet.objects.filter(user_diet_id=pk, food__deleted=False)
                for diet_item in contains_food_in_diet:
                    diet_item.pk = None
                    diet_item.user_diet = new_user_diet
                    diet_item.save()
                return redirect('dietcalc:diet_view', slug=new_user_diet.slug)
            else:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            raise Http404()
    elif request.method == 'GET':
        user_diet = UserDiet.objects.get(pk=pk)
        if user_diet.user == request.user:
            user_diet.pk = None
            user_diet.name = ("Копия " + user_diet.name)[:255]
            form = CreateAndUpdateMyDietForm(instance=user_diet)
            return render(request, 'dietcalc/diets/my_diet_create.html',
                          {"form": form, "menuhome": MenuHome.objects.all(),
                           "description": "Cтраница с информацией для связи.",
                           "title": "Обновление пользовательской диеты", "button": "Создать копию диеты"})
        else:
            raise Http404()


def copy_my_diet_to_user(request, pk):
    if request.user.is_staff:
        if request.method == 'POST':
            if UserDiet.objects.get(pk=pk).user == request.user:
                print(request.POST)
                form = CopyMyDietToUserForm(request.POST)
                if form.is_valid():
                    new_slug_userdiet = slugify(form.cleaned_data['name'])[:90] + '-' + ''.join(
                        random.choices(string.ascii_uppercase + string.ascii_lowercase, k=10))
                    data_user_diet = {**form.cleaned_data, **{'user': form.cleaned_data['user'], 'slug': new_slug_userdiet}}
                    new_user_diet = UserDiet.objects.create(**data_user_diet)
                    contains_food_in_diet = Diet.objects.filter(user_diet_id=pk, food__deleted=False)
                    for diet_item in contains_food_in_diet:
                        diet_item.pk = None
                        diet_item.user_diet = new_user_diet
                        diet_item.save()
                    return redirect('dietcalc:mydiets')
                else:
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                raise Http404()
        elif request.method == 'GET':
            user_diet = UserDiet.objects.get(pk=pk)
            if user_diet.user == request.user:
                user_diet.pk = None
                user_diet.name = ("Копия " + user_diet.name[:200] + " (поделился: " + request.user.__str__() + ") ")
                form = CopyMyDietToUserForm(instance=user_diet)
                return render(request, 'dietcalc/diets/my_diet_create.html',
                              {"form": form, "menuhome": MenuHome.objects.all(),
                               "description": "Cтраница с информацией для связи.",
                               "title": "Обновление пользовательской диеты", "button": "Создать копию диеты"})
            else:
                raise Http404()

    else:
        raise Http404()
