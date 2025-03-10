from django.db import models
from django.conf import settings

class Residence(models.Model):
    # Fields for residence characteristics (as described in roadmap)
    number_of_rooms = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"Residence at {self.location} - {self.number_of_rooms} rooms"

class AdminProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, help_text="Administrator's phone number")

    def __str__(self):
        return f"Admin Profile for {self.user.username}"
