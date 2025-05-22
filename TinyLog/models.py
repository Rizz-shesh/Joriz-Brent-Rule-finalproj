
from django.contrib.auth.models import User
from django.db import models

class Patient(models.Model):
    name = models.CharField(max_length=255)
    religion = models.CharField(max_length=100)
    place_of_birth = models.CharField(max_length=255)
    pediatrician = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    sex = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])
    birth_weight = models.DecimalField(max_digits=10, decimal_places=2)
    mother_maiden_name = models.CharField(max_length=255)
    birth_height = models.DecimalField(max_digits=10, decimal_places=2)
    father_name = models.CharField(max_length=255)
    address = models.CharField(max_length=500)

    def __str__(self):
        return self.name

class ImmunizationRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    vaccine = models.CharField(max_length=100)
    dose = models.CharField(max_length=100)
    vaccine_batch_number = models.CharField(max_length=50)
    date_of_administration = models.DateField()
    facility_name = models.CharField(max_length=255)
    administering_provider = models.CharField(max_length=255)
    remarks = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.patient.name} - {self.vaccine}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, default="Healthcare Provider")
    username = models.CharField(max_length=100, unique=True, null=True)

    def __str__(self):
        return self.user.username
    
class MedicalHospitalizationRecord(models.Model):
    TYPE_CHOICES = [
        ('OUT PATIENT', 'Out patient'),
        ('IN PATIENT', 'In patient'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, null=True)  # Ensure this field exists
    name_of_facility = models.CharField(max_length=200)
    date_of_visit = models.DateField()
    name_of_physician = models.CharField(max_length=200)
    chief_complaint = models.CharField(max_length=200)
    nurses_notes = models.TextField(blank=True, null=True)
    medical_impression = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.patient.name} - {self.type} ({self.date_of_visit})"