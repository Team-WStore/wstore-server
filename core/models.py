from email.policy import default
from django.db import models

# Create your models here.
class ImageItem(models.Model):
    image = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.image

class ItemCarrousel(models.Model):
    name = models.CharField(max_length=50)
    image = models.URLField(max_length=500)
    url = models.CharField(max_length=200)
    description = models.CharField(max_length=500, default='')
    created = models.DateTimeField(auto_now_add=True, null= True, blank=True)

    class Meta:
        ordering = ['created']
    
    def __str__(self):
        return self.name