__all__ = ["MyDietsView", "UserDietView", "PublicDietView"]

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Sum, Q

from django.views.generic import ListView, DetailView
from django.http import Http404


from siteapp.models import MenuHome

from dietcalc.models import Food, UserDiet, Diet

class MyDietsView(LoginRequiredMixin, ListView):
    model = UserDiet
    template_name = "dietcalc/diets/my_diets_view.html"
    context_object_name = "userdiets"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return UserDiet.objects.filter(deleted=False, user=self.request.user)
        else:
            return self

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Мои диеты"
        context['menuhome'] = MenuHome.objects.all()
        return context


class UserDietView(LoginRequiredMixin, DetailView):
    model = UserDiet
    template_name = 'dietcalc/diets/my_diet_view.html'
    context_object_name = "userdiet"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menuhome'] = MenuHome.objects.all()
        context['foods'] = Food.objects.filter(Q(deleted=False) & (Q(is_published=True) | Q(user=self.request.user))).order_by('-special_food','name')
        context_diets = Diet.objects.filter(user_diet_id=UserDiet.objects.get(slug=self.kwargs['slug']).id).annotate(
            f_protein=F('food__protein') * F('count') / 100, f_fat=F('food__fat') * F('count') / 100,
            f_carbohydrates=F('food__carbohydrates') * F('count') / 100,
            f_calories=F('food__calories') * F('count') / 100)
        if context_diets.count() > 0:
            context['diets'] = context_diets
            context['diets_aggregate'] = context_diets.aggregate(sum_protein=Sum('f_protein'), sum_fat=Sum('f_fat'),
                                                                 sum_carbohydrates=Sum('f_carbohydrates'),
                                                                 sum_calories=Sum('f_calories'))
            diet_procent_and_sum_weight = {
                "procent_protein": context['diets_aggregate']['sum_protein'] * 400 / context['diets_aggregate'][
                    'sum_calories'],
                "procent_fat": context['diets_aggregate']['sum_fat'] * 910 / context['diets_aggregate']['sum_calories'],
                "procent_carbohydrates": context['diets_aggregate']['sum_carbohydrates'] * 400 /
                                         context['diets_aggregate']['sum_calories'],
                "sum_protein_weight": float(context['diets_aggregate']['sum_protein']) / context['userdiet'].weight,
                "sum_fat_weight": float(context['diets_aggregate']['sum_fat']) / context['userdiet'].weight,
                "sum_carbohydrates_weight": float(context['diets_aggregate']['sum_carbohydrates']) / context[
                    'userdiet'].weight,
                "sum_calories_weight": context['diets_aggregate']['sum_calories'] / context['userdiet'].weight
                }
            context['diets_aggregate'].update(diet_procent_and_sum_weight)
        return context


class PublicDietView(DetailView):
    model = UserDiet
    template_name = 'dietcalc/diets/public_diet_view.html'
    context_object_name = "userdiet"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menuhome'] = MenuHome.objects.all()
        try:
            user_diet_id = UserDiet.objects.get(slug=self.kwargs['slug'], is_published=True).id
        except UserDiet.DoesNotExist:
            raise Http404()
        context_diets = Diet.objects.filter(user_diet_id=user_diet_id).annotate(
            f_protein=F('food__protein') * F('count') / 100, f_fat=F('food__fat') * F('count') / 100,
            f_carbohydrates=F('food__carbohydrates') * F('count') / 100,
            f_calories=F('food__calories') * F('count') / 100)
        if context_diets.count() > 0:
            context['diets'] = context_diets
            context['diets_aggregate'] = context_diets.aggregate(sum_protein=Sum('f_protein'), sum_fat=Sum('f_fat'),
                                                                 sum_carbohydrates=Sum('f_carbohydrates'),
                                                                 sum_calories=Sum('f_calories'))
            diet_procent_and_sum_weight = {
                "procent_protein": context['diets_aggregate']['sum_protein'] * 400 / context['diets_aggregate'][
                    'sum_calories'],
                "procent_fat": context['diets_aggregate']['sum_fat'] * 910 / context['diets_aggregate']['sum_calories'],
                "procent_carbohydrates": context['diets_aggregate']['sum_carbohydrates'] * 400 /
                                         context['diets_aggregate']['sum_calories'],
                "sum_protein_weight": float(context['diets_aggregate']['sum_protein']) / context['userdiet'].weight,
                "sum_fat_weight": float(context['diets_aggregate']['sum_fat']) / context['userdiet'].weight,
                "sum_carbohydrates_weight": float(context['diets_aggregate']['sum_carbohydrates']) / context[
                    'userdiet'].weight,
                "sum_calories_weight": context['diets_aggregate']['sum_calories'] / context['userdiet'].weight
                }
            context['diets_aggregate'].update(diet_procent_and_sum_weight)
        return context

