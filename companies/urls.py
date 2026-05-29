from django.urls import path
from . import views

urlpatterns = [
    path('companies/', views.company_list, name='company_list'),
    path('companies/<slug:slug>/', views.company_detail, name='company_detail'),
    path('companies/<slug:slug>/apply/', views.apply_company, name='apply_company'),
    path('companies/slot/<int:slot_id>/book/', views.book_slot, name='book_slot'),
    path('companies/booking/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('applications/', views.my_applications, name='my_applications'),
]
