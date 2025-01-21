from django.db import models

class Patient(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey('Doctor.Doctor', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=[
        ('Scheduled', 'Scheduled'),
        ('Rescheduled', 'Rescheduled'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed')
    ])
    medical_history_added = models.BooleanField(default=False)
    prescription_added = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.patient} - {self.doctor} on {self.date}"

class MedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    medications = models.TextField()
    allergies = models.TextField(blank=True)
    treatment_history = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Medical History for {self.patient}"


class Billing(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Paid', 'Paid')])
    invoice_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Bill for {self.patient} - {self.amount}"

class HealthResource(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    link = models.URLField(blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    doctor = models.ForeignKey('Doctor.Doctor', on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return self.title
