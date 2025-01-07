from django.urls import path
from . import views

urlpatterns = [
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('create_doctor/', views.create_doctor, name='create_doctor'),
    path('add-medical-history/<int:appointment_id>/', views.add_medical_history, name='medical_history'),
    path('create_bill/<int:appointment_id>/', views.create_bill, name='create_bill'),      
]
