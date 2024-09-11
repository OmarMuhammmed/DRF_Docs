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
    last_name = serializers.SerializerMethodField(read_only=True)
    class Meta :
        model = Client
        fields = ['pk','reservation','name','phone','last_name']

    def get_last_name(self,obj):
        return f"{obj.name} {obj.last_name}"