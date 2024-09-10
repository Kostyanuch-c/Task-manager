from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render


@login_required
def statuses(request):
    return render(request, 'tasks/statuses/lits_statuses.html')
