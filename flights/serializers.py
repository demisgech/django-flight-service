from rest_framework import serializers

from .models import (
    Airport,
    Flight,
    Promotion
)

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ['id','name','city','country','iata_code',
                  'icao_code','latitude','longitude']


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ['id','title','discount','start_date','end_date']


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ['id','airline','flight_number','departure_time',
                  'departure_airport','arrival_airport','arrival_time',
                  'duration','seat_capacity','price']