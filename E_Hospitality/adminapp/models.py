from django.db import models

from accounts.models import User

# Create your models here.


class Facility(models.Model):
    hosp_name = models.CharField(max_length=255)
    address = models.TextField(max_length=255)
    contact = models.CharField(max_length=20)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f" {self.hosp_name}"
