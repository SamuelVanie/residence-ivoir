from django.db import models
from django.conf import settings

class Residence(models.Model):
    # Fields for residence characteristics (as described in roadmap)
    name = models.CharField(max_length=255)
    number_of_rooms = models.IntegerField()
    promotional_price = models.DecimalField(max_digits=10, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True, help_text="Residence available for getting booked rn?")
    location = models.CharField(max_length=255, default='Yamoussoukro')
    description = models.TextField()
    image = models.ImageField(upload_to='residence_images/', blank=True)

    def __str__(self):
        return f"Residence {self.name} at {self.location} - {self.number_of_rooms} rooms"

class AdminProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, help_text="Administrator's phone number")

    def __str__(self):
        return f"Admin Profile for {self.user.username}"
