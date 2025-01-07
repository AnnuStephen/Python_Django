from django.db import models

from Patient.models import Patient


class Doctor(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name} - {self.specialization}"


class EPrescription(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medication = models.TextField()
    dosage = models.TextField()
    prescription_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Prescription by {self.doctor} for {self.patient}"
