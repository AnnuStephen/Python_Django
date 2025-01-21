from django import forms
from .models import Patient, Appointment, MedicalHistory, Billing, HealthResource

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'date_of_birth', 'address', 'phone_number', 'email']

class AppointmentForm(forms.ModelForm):    
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time']
    
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d']
    )
    time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        input_formats=['%H:%M']
    )

class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        fields = ['diagnosis', 'medications', 'allergies', 'treatment_history']

class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields = ['patient', 'amount', 'payment_status']

class HealthResourceForm(forms.ModelForm):
    class Meta:
        model = HealthResource
        fields = [ 'content', 'link']
