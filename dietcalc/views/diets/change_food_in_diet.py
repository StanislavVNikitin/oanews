__all__ = ["change_food_in_diet"]

from django.shortcuts import redirect
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required

from dietcalc.models import Diet

@login_required()
def change_food_in_diet(request, pk):
    if request.method == 'POST':
        if request.POST['count']:
            try:
                updateitemdiet = Diet.objects.get(pk=pk)
            except Diet.DoesNotExist:
                raise Http404()
            else:
                if updateitemdiet.user_diet.user == request.user and int(request.POST['count']) > 0 and int(request.POST['count']) < 1000 and updateitemdiet.count != \
                        request.POST['count']:
                    updateitemdiet.count = request.POST['count']
                    updateitemdiet.save()
                else:
                    raise Http404()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect("dietcalc:mydiets")