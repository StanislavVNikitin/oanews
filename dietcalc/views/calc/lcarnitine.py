__all__ = ["CalcLCarnitine"]

from django.views.generic import TemplateView

from siteapp.models import MenuHome


class CalcLCarnitine(TemplateView):
    template_name = 'dietcalc/calc/calc_lcarnitine.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menuhome'] = MenuHome.objects.all()
        return context