from django.db import models

# Create your models here.
from django.db import models

class Residence(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, default='Yamoussoukro')
    description = models.TextField()
    rooms = models.IntegerField()
    price = models.IntegerField()
    promotional_price = models.IntegerField(null=True, blank=True) # nullable
    is_available = models.BooleanField(default=True)
    next_availability = models.DateField(null=True, blank=True) # nullable
    image = models.ImageField(upload_to='residence_images/') # You might want to adjust upload_to

    def __str__(self):
        return self.name
