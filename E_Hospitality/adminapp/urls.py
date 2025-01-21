from django.urls import path
from . import views

urlpatterns = [
     path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
     path('doctor_details/<int:user_id>/', views.doctor_details, name='doctor_details'),
     path('patient_details/<int:user_id>/', views.patient_details, name='patient_details'),
    
     path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
     path('create_users/', views.create_user, name='create_users'),
     path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),

     path('create_appointment/<int:patient_id>/', views.admin_create_appointment, name='admin_create_appointment'),   
     path('appointments_edit/<int:appointment_id>/', views.edit_appointment, name='edit_appointment'),
     path('appointments_cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    
     path('create-facility/', views.create_facility, name='create_facility'),
     path('edit/<int:pk>/', views.edit_facility, name='edit_facility'),
     path('delete_facility/<int:pk>/', views.delete_facility, name='delete_facility'),
     


     
]
