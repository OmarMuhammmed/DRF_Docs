from django.contrib import admin
from .models import Client, Reservation, Movie
# Register your models here.

admin.site.register(Client)
admin.site.register(Reservation)
admin.site.register(Movie)
  