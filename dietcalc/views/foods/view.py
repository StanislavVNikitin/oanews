__all__ = ["MyFoodsView", "UserFoodView"]

from django.contrib.auth.mixins import LoginRequiredMixin
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