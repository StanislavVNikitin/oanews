__all__ = ["DeleteMyFood"]

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from siteapp.models import MenuHome
from dietcalc.models import Food

class DeleteMyFood(LoginRequiredMixin, DeleteView):
    model = Food
    success_url = reverse_lazy('dietcalc:myfoods')
    template_name = 'dietcalc/foods/food_confirm_delete.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Food.objects.filter(deleted=False, user=self.request.user)
        else:
            return self

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Удаление пользовательского продукта"
        context['menuhome'] = MenuHome.objects.all()
        return context