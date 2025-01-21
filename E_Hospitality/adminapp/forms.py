from django import forms

from accounts.models import User
from .models import Facility

class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = ['hosp_name', 'address', 'contact']


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'role']
        widgets = {
            'password': forms.PasswordInput(),
        }