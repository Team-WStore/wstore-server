from django.db import models

# Create your models here.
class ItemCarrousel(models.Model):
    name = models.CharField(max_length=50)
    #image = models.URLField(max_length=500)
    image = models.ImageField(upload_to='carrousel/', null=True, blank=True)
    url = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=False, null= True, blank=True)

    class Meta:
        ordering = ['created']
    
    def __str__(self):
        return self.name