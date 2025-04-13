from django.shortcuts import render, get_object_or_404
from .models import Residence
from .models import AdminProfile # Import AdminProfile
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseBadRequest, Http404
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from urllib.parse import quote
import logging

logger = logging.getLogger(__name__)

def get_admin_phone():

    admin_phone_number = "+2250787876981"
    try:
        admin_profile = AdminProfile.objects.first()
        if admin_profile and admin_profile.phone_number:
            phone = admin_profile.phone_number.replace(" ", "").replace("-", "")
            admin_phone_number = phone
    except AdminProfile.DoesNotExist:
        logger.warning("AdminProfile not found, using fallback phone number.")
        pass
    except Exception as e:
        logger.error(f"Error fetching admin phone number: {e}")
        pass

    # Clean for wa.me link (remove non-digits)
    cleaned_phone_for_wa = ''.join(filter(str.isdigit, admin_phone_number))
    return cleaned_phone_for_wa


def home(request):
    return render(request, 'home.html')

def residence_list(request):
    residence_list = Residence.objects.all().order_by('name')
    paginator = Paginator(residence_list, 6) # Show 6 residences per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Pass the page object instead of the full list
    return render(request, 'residence/residence_list.html', {'page_obj': page_obj})

def filter_residences_by_rooms(request, rooms):
    residences = Residence.objects.filter(number_of_rooms=rooms)
    data = [{
        'id': residence.id,
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
        'id': residence.id,
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



def whatsapp_contact_link(request):
    admin_phone_number = get_admin_phone()
    message = request.POST.get('question', '')
    whatsapp_message = quote(message)
    whatsapp_link = f"https://wa.me/{admin_phone_number}?text={whatsapp_message}"
    return HttpResponseRedirect(whatsapp_link)


@require_POST
def generate_whatsapp_reservation_link(request):
    try:
        residence_id = request.POST.get('residence_id')
        days = request.POST.get('days')
        arrival_date = request.POST.get('arrival_date')

        # Basic validation
        if not residence_id or not days or not arrival_date:
            logger.warning("generate_whatsapp_reservation_link: Missing POST data.")
            return HttpResponseBadRequest("Données manquantes.") # Bad request

        # Fetch residence securely from DB using the ID
        residence = get_object_or_404(Residence, pk=int(residence_id))

        # Get admin phone number
        admin_phone_number = get_admin_phone()
        if not admin_phone_number:
             logger.error("generate_whatsapp_reservation_link: Admin phone number not configured.")
             # Handle error appropriately - maybe redirect to an error page or show message
             return HttpResponseBadRequest("Erreur de configuration du contact.")

        # --- Build Message using SERVER-SIDE data ---
        message_parts = [
            "Bonjour, je souhaiterais réserver la résidence suivante :",
            f"Nom: {residence.name}", # From DB
        ]
        if residence.location:
            message_parts.append(f"Localisation: {residence.location}") # From DB
        if residence.number_of_rooms:
            message_parts.append(f"Nombre de chambres: {residence.number_of_rooms}") # From DB

        price_str = f"{residence.price} FCFA/nuit" # From DB
        if residence.promotional_price:
            price_str += f" (Promo: {residence.promotional_price} FCFA/nuit)" # From DB
        message_parts.append(f"Prix: {price_str}")
        message_parts.append("----")
        message_parts.append(f"Durée souhaitée: {days} jour(s)") # From User Input
        message_parts.append(f"Date d'arrivée prévue: {arrival_date}") # From User Input
        message_parts.append("----")
        message_parts.append("Merci!")

        message = "\n".join(message_parts)
        whatsapp_message = quote(message) # URL Encode

        # Construct the final link
        whatsapp_link = f"https://wa.me/{admin_phone_number}?text={whatsapp_message}"

        # Redirect the user to WhatsApp
        return HttpResponseRedirect(whatsapp_link)

    except (ValueError, TypeError):
        logger.warning(f"generate_whatsapp_reservation_link: Invalid residence_id format: {request.POST.get('residence_id')}")
        return HttpResponseBadRequest("ID de résidence invalide.")
    except Http404:
        logger.warning(f"generate_whatsapp_reservation_link: Residence not found for ID: {request.POST.get('residence_id')}")
        # Optionally redirect to an error page or the list page with a message
        return HttpResponseBadRequest("Résidence non trouvée.")
    except Exception as e:
        logger.error(f"Error in generate_whatsapp_reservation_link: {e}", exc_info=True)
        # Generic error for unexpected issues
        return HttpResponseBadRequest("Une erreur est survenue lors de la génération du lien.")
