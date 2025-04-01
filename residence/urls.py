from django.urls import path
from . import views

urlpatterns = [
    path('', views.residence_list, name='residence_list'),
    path('filter_by_rooms/rooms<int:rooms>/', views.filter_residences_by_rooms, name='filter_residences'),
    path('filter_by_budget/', views.filter_residences_by_budget, name='filter_residences_by_budget'),
    path('contact/whatsapp/', views.whatsapp_contact_link, name='whatsapp_contact_link'),
    path('reserve/whatsapp/', views.whatsapp_reserve_link, name='whatsapp_reserve_link')
]
