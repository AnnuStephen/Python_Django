from django.urls import path
from . import views

urlpatterns = [
    path('patient-dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('create-appointment/', views.create_appointment, name='create_appointment'),
    path('create_profile/', views.create_profile, name='create_profile'),
    path('pay_bill/<int:bill_id>/', views.pay_bill, name='pay_bill'),    
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-cancelled/', views.payment_cancelled, name='payment_cancelled'),  
]
