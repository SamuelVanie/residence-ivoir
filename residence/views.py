from django.shortcuts import render
from .models import Residence

def residence_list(request):
    residences = Residence.objects.all()
    return render(request, 'residence/residence_list.html', {'residences': residences})
