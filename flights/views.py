from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Airport,
    Flight,
    Promotion
)
from .serializers import (
    AirportSerializer,
    FlightSerializer,
    PromotionSerializer,
)

# Class based view
class AirportList(APIView):
    
    def get(self,request:Request)->Response:
        queryset = Airport.objects.all()
        serializer = AirportSerializer(queryset, many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
        
    def post(self,request:Request)->Response:
        serializer = AirportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data,status=status.HTTP_201_CREATED)


class AirportDetail(APIView):
    
    def get(self,request:Request,id:int)->Response:
        airport = get_object_or_404(Airport,pk=id)
        serializer = AirportSerializer(airport)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request:Request,id:int)->Response:
        airport = get_object_or_404(Airport,pk=id)
        serializer = AirportSerializer(airport,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
    def delete(self,request:Request,id:int)->Response:
        airport = get_object_or_404(Airport,pk=id)
        airport.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Function based view

@api_view(['GET','POST'])
def airport_list(request:Request)-> Response:
    if request.method == "GET":
        queryset = Airport.objects.all()
        serializer = AirportSerializer(queryset,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        serializer = AirportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data,status=status.HTTP_201_CREATED)
    

@api_view(['GET','PUT','DELETE'])
def airport_detail(request:Request,id:int) -> Response:
    airport = get_object_or_404(Airport,pk=id)
    if request.method == "GET":
        serializer = AirportSerializer(airport)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
    elif request.method == "PUT":
        serializer = AirportSerializer(airport,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
    elif request.method == "DELETE":
        airport.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Class based View

class PromotionList(APIView):
    
    def get(self,request:Request)->Response:
        queryset = Promotion.objects.all()
        serializer = PromotionSerializer(queryset,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request:Request)->Response:
        serializer = PromotionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data,status=status.HTTP_201_CREATED)
    

class PromotionDetail(APIView):
    
    def get(self,request:Request,id:int)->Response:
        promotion = get_object_or_404(Promotion,pk=id)
        serializer = PromotionSerializer(promotion)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request:Request,id:int)->Response:
        promotion = get_object_or_404(Promotion,pk=id)
        serializer = PromotionSerializer(promotion,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
    def delete(self,request:Request,id:int):
        promotion = get_object_or_404(Promotion,pk=id)
        if promotion.flights.count() > 0:
            return Response({"error":"Promotion cannot be deleted because it is associated with one or more flights"})
        promotion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Function based view

@api_view(['GET','POST'])
def promotion_list(request:Request)->Response:
    if request.method == "GET":
        queryset = Promotion.objects.all()
        serializer = PromotionSerializer(queryset,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        serializer = PromotionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data,status=status.HTTP_201_CREATED)
    

@api_view(['GET','PUT','DELETE'])
def promotion_detail(request:Request,id:int)->Response:
    promotion = get_object_or_404(Promotion,pk=id)
    if request.method == "GET":
        serializer = PromotionSerializer(promotion)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
    elif request.method == "PUT":
        serializer = PromotionSerializer(promotion,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
    elif request.method == "DELETE":
        if promotion.flights.count() > 0:
            return Response({"error":"Promotion cannot be deleted because it contains more than on flights"},status=status.HTTP_400_BAD_REQUEST)
        promotion.delete()
        return Response(status=status.HTTP_201_CREATED)
        

class FlightList(APIView):
    
    def get(self,request:Request)->Response:
        queryset = Flight.objects.all()
        serializer = FlightSerializer(queryset,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request:Request)->Response:
        serializer = FlightSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data,status=status.HTTP_201_CREATED)


class FlightDetail(APIView):
    
    def get(self,request:Request,id:int)->Response:
        flight = get_object_or_404(Flight,pk=id)
        serializer = FlightSerializer(flight)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request:Request,id:int)->Response:
        flight = get_object_or_404(Flight,pk=id)
        serializer = FlightSerializer(flight,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
    def delete(self,request:Request,id:int)->Response:
        flight = get_object_or_404(Flight,pk=id)
        flight.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET','POST'])
def flight_list(request:Request)->Response:
    if request.method == "GET":
        queryset = Flight.objects.all()
        serializer = FlightSerializer(queryset,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        serializer = FlightSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data,status=status.HTTP_201_CREATED)
    

@api_view(['GET','PUT','DELETE'])
def flight_detail(request:Request,id:int)->Response:
    flight = get_object_or_404(Flight,pk=id)
    if request.method == "GET":
        serializer = FlightSerializer(flight)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
    elif request.method == "PUT":
        serializer = FlightSerializer(flight,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
    elif request.method == "DELETE":
        flight.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    