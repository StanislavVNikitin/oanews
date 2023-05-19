__all__ = ["delete_food_to_diet"]

from django.shortcuts import redirect
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from dietcalc.models import Diet

@login_required()
def delete_food_to_diet(request, pk):
    if request.method == 'GET':
        try:
            delete_food_in_diet = Diet.objects.get(pk=pk)
        except Diet.DoesNotExist:
            raise Http404()
        else:
            if delete_food_in_diet.user_diet.user == request.user:
                delete_food_in_diet.delete()
            else:
                raise Http404()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect("dietcalc:mydiets")