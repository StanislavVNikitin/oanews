__all__ = ["MyFoodsView", "UserFoodView", "ajax_food"]

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import ListView, DetailView


from siteapp.models import MenuHome

from dietcalc.models import Food


class MyFoodsView(LoginRequiredMixin, ListView):
    model = Food
    template_name = "dietcalc/foods/my_foods_view.html"
    context_object_name = "userfoods"
    paginate_by = 50

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Food.objects.filter(deleted=False, user=self.request.user)
        else:
            return self

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Мои продукты"
        context['menuhome'] = MenuHome.objects.all()
        return context


class UserFoodView(LoginRequiredMixin, DetailView):
    model = Food
    template_name = 'dietcalc/foods/my_food_view.html'
    context_object_name = "userfood"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menuhome'] = MenuHome.objects.all()
        return context

@login_required()
def ajax_food(request, user_pk):
    if (request.GET['term'] and not request.GET['term'] == ""):
        ajax_foods = Food.objects.filter(
            Q(Q(deleted=False) & (Q(is_published=True) | Q(user__pk=user_pk))) & Q(
                name__iregex=request.GET['term'])).order_by('-special_food', 'name')
    else:
        ajax_foods = Food.objects.filter(
            Q(Q(deleted=False) & (Q(is_published=True) | Q(user__pk=user_pk)))).order_by('-special_food', 'name')
    data = {food.name: {'label': food.name, 'id': food.pk} for food in ajax_foods}
    if request.method == 'GET':
        return JsonResponse(data)
