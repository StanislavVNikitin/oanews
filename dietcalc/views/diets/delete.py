__all__ = ["DeleteMyDiet"]

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from siteapp.models import MenuHome

from dietcalc.models import UserDiet

class DeleteMyDiet(LoginRequiredMixin, DeleteView):
    model = UserDiet
    success_url = reverse_lazy('dietcalc:mydiets')
    template_name = 'dietcalc/diets/userdiet_confirm_delete.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return UserDiet.objects.filter(deleted=False, user=self.request.user)
        else:
            return self

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Удаление пользовательской диеты"
        context['menuhome'] = MenuHome.objects.all()
        return context