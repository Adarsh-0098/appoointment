from django.db import models

# Doctor model
class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    availability = models.DateTimeField()  # For simplicity, one available time slot
    location = models.CharField(max_length=100, default="")  # Optional field for location

    def __str__(self):
        return f"{self.name} - {self.specialty}"

# Appointment model
class Appointment(models.Model):
    patient_name = models.CharField(max_length=100)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_time = models.DateTimeField()
    symptoms = models.TextField()

    def __str__(self):
        return f"Appointment for {self.patient_name} with Dr. {self.doctor.name}"
