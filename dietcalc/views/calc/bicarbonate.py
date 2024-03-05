__all__ = ["CalcBicarbonate"]

from django.views.generic import TemplateView

from siteapp.models import MenuHome


class CalcBicarbonate(TemplateView):
    template_name = 'dietcalc/calc/calc_bicarbonate.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menuhome'] = MenuHome.objects.all()
        context['title'] = 'Калькулятор для пересчета гидрокарбоната натрия(сода)'
        return context