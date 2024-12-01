from rest_framework import serializers
from .models import Movie, Reservation, Client


class MovieSerializer(serializers.ModelSerializer):

    class Meta :
        model = Movie
        fields = ['pk','hall','movie']

    def to_representation(self, instance):

        """Convert `movie` to lowercase."""

        ret = super().to_representation(instance)
        ret['movie'] = ret['movie'].lower()
        return ret
        
class ReservationSerializer(serializers.ModelSerializer):

    class Meta :
        model = Reservation
        fields = ['pk','client','movie']

    # Works When Write in views.py serilzer.save() 
    def create(self, validated_data):
        return Reservation.objects.create(validated_data)  

     # Works When Write in views.py serilzer.save()
    def update(self, instance, validated_data):
        instance.client = validated_data.get('client', instance.client)
        return instance     

    

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

    
