from django import forms
from .models import Doctor, EPrescription

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name','facility', 'specialization', 'contact_number', 'email']
        
class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'specialization', 'contact_number', 'email']


class EPrescriptionForm(forms.ModelForm):
    class Meta:
        model = EPrescription
        fields = [ 'medication', 'dosage']
