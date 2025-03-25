from django.shortcuts import render
from .models import Residence
from django.http import JsonResponse

def home(request):
    return render(request, 'home.html')

def residence_list(request):
    residences = Residence.objects.all()
    return render(request, 'residence/residence_list.html', {'residences': residences})

def filter_residences_by_rooms(request, rooms):
    residences = Residence.objects.filter(number_of_rooms=rooms)
    data = [{
        'name': residence.name,
        'number_of_rooms': residence.number_of_rooms,
        'price': float(residence.price),
        'location': residence.location,
        'image_url': request.build_absolute_uri(residence.image.url) if residence.image else None,
    } for residence in residences]
    return JsonResponse(data, safe=False)

def filter_residences_by_budget(request):
    min_budget = request.GET.get('min_budget')
    max_budget = request.GET.get('max_budget')

    if min_budget and max_budget:
        residences = Residence.objects.filter(price__gte=min_budget, price__lte=max_budget)
    else:
        residences = Residence.objects.all()

    data = [{
        'name': residence.name,
        'number_of_rooms': residence.number_of_rooms,
        'price': float(residence.price),
        'location': residence.location,
        'image_url': request.build_absolute_uri(residence.image.url) if residence.image else None,
    } for residence in residences]
    return JsonResponse(data, safe=False)
