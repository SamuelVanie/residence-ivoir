from django.shortcuts import render
from .models import Residence
from django.http import JsonResponse

def residence_list(request):
    residences = Residence.objects.all()
    return render(request, 'residence/residence_list.html', {'residences': residences})

def filter_residences_by_rooms(request):
    rooms = request.GET.get('rooms')
    residences = Residence.objects.filter(number_of_rooms=rooms)
    data = [{
        'name': residence.name,
        'number_of_rooms': residence.number_of_rooms,
        'price': residence.price,
        'location': residence.location,
        'image_url': request.build_absolute_uri(residence.image.url) if residence.image else None,
    } for residence in residences]
    return JsonResponse(data, safe=False)
