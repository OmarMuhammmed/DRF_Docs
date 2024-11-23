from rest_framework import serializers
from .models import Movie, Reservation, Client


class MovieSerializer(serializers.ModelSerializer):

    class Meta :
        model = Movie
        fields = ['pk','hall','movie']
        
class ReservationSerializer(serializers.ModelSerializer):

    class Meta :
        model = Reservation
        fields = ['pk','client','movie']

    

class ClientSerializer(serializers.ModelSerializer):
    class Meta :
        model = Client
        fields = ['pk','reservation','name','phone']


    # validate filed example 
    def validate_phone(self, phone_value):
        str_phone_value = str(phone_value)
        if len(str_phone_value) != 11 :
            raise serializers.ValidationError("Phone number must be 11 digits long")
        else :
            return phone_value

    
