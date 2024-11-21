from rest_framework import serializers
from .models import Movie, Reservation, Client


class MovieSerializer(serializers.ModelSerializer):

    class Meta :
        model = Movie
        fields = '__all__'
        
class ReservationSerializer(serializers.ModelSerializer):

    class Meta :
        model = Reservation
        fields = '__all__'
        
class ClientSerializer(serializers.ModelSerializer):
    class Meta :
        model = Client
        fields = ['pk','reservation','name','phone']
