from django.shortcuts import render, get_object_or_404
from .models import Residence
from .models import AdminProfile # Import AdminProfile
from django.http import HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator
from urllib.parse import quote

def home(request):
    return render(request, 'home.html')

def residence_list(request):
    residence_list = Residence.objects.all()
    paginator = Paginator(residence_list, 6) # Show 6 residences per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Pass the page object instead of the full list
    return render(request, 'residence/residence_list.html', {'page_obj': page_obj})

def filter_residences_by_rooms(request, rooms):
    residences = Residence.objects.filter(number_of_rooms=rooms)
    data = [{
        'name': residence.name,
        'number_of_rooms': residence.number_of_rooms,
        'price': float(residence.price),
        'location': residence.location,
        'image_url': request.build_absolute_uri(residence.image.url) if residence.image else None,
        'description': residence.description, # Added description
        'is_available': residence.is_available, # Added is_available
        'promotional_price_per_night': float(residence.promotional_price) if residence.promotional_price else None, # Added promo price
    } for residence in residences]
    return JsonResponse(data, safe=False)

def filter_residences_by_budget(request):
    min_budget = request.GET.get('min_budget')
    max_budget = request.GET.get('max_budget')

    if min_budget and max_budget:
        residences = Residence.objects.filter(price__gte=min_budget, price__lte=max_budget)
    elif min_budget: # Only min budget
        residences = Residence.objects.filter(price__gte=min_budget)
    elif max_budget: # Only max budget
        residences = Residence.objects.filter(price__lte=max_budget)
    else:
        residences = Residence.objects.all()

    data = [{
        'name': residence.name,
        'number_of_rooms': residence.number_of_rooms,
        'price': float(residence.price),
        'location': residence.location,
        'image_url': request.build_absolute_uri(residence.image.url) if residence.image else None,
        'description': residence.description, # Added description
        'is_available': residence.is_available, # Added is_available
        'promotional_price_per_night': float(residence.promotional_price) if residence.promotional_price else None, # Added promo price
    } for residence in residences]
    return JsonResponse(data, safe=False)

def whatsapp_reserve_link(request, residence_id):
    admin_phone_number = "+2250748552211" # Fallback number
    try:
        admin_profile = AdminProfile.objects.first() # Assuming only one admin profile
        if admin_profile and admin_profile.phone_number:
            admin_phone_number = admin_profile.phone_number
    except AdminProfile.DoesNotExist:
        pass # Use default number if AdminProfile not found

    residence = get_object_or_404(Residence, pk=residence_id)
    message_parts = [
        "Bonjour, je suis intéressé(e) par la résidence suivante :",
        f"Nom: {residence.name}",
        f"Localisation: {residence.location}",
        f"Nombre de chambres: {residence.number_of_rooms}",
        f"Prix: {residence.price} FCFA/nuit",
    ]
    if residence.promotional_price:
        message_parts.append(f"Prix promotionnel: {residence.promotional_price} FCFA/nuit")

    message = "\n".join(message_parts)
    whatsapp_message = quote(message)
    whatsapp_link = f"https://wa.me/{admin_phone_number}?text={whatsapp_message}"
    return HttpResponseRedirect(whatsapp_link)

def whatsapp_contact_link(request):
    admin_phone_number = "+2250748552211" # Fallback number
    try:
        admin_profile = AdminProfile.objects.first() # Assuming only one admin profile
        if admin_profile and admin_profile.phone_number:
            admin_phone_number = admin_profile.phone_number
    except AdminProfile.DoesNotExist:
        pass # Use default number if AdminProfile not found
    message = request.POST.get('question', '')
    whatsapp_message = quote(message) # URL encode the message
    whatsapp_link = f"https://wa.me/{admin_phone_number}?text={whatsapp_message}"
    return HttpResponseRedirect(whatsapp_link)
