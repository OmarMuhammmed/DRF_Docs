from django.db import models
import datetime 
from django.db.models.signals import post_save
from django.dispatch import receiver 
from rest_framework.authtoken.models import Token
from django.conf import settings
# Client -- Movie -- Reservation.

class Movie(models.Model):
    hall = models.CharField(max_length=10)
    movie = models.CharField(max_length=50)
    

    
    def __str__(self):
        return self.movie
    
class Client(models.Model):
    name = models.CharField( max_length=50)
    phone = models.IntegerField()

    
    def __str__(self):
        return self.name
    
    

class Reservation(models.Model):
    client = models.ForeignKey(Client, related_name='reservation', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='reservation', on_delete=models.CASCADE)
   
    def __str__(self):
       return f"{self.client}_{self.movie}"

# signals
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def token_created(sender, instance, created, **kwars):
    if created :
        Token.objects.create(user=instance)