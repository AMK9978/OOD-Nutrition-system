from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from .serializers import UserSerializer, FoodSerializer
from .models import User, Food, FoodReserve


class FoodProgramViewSet(viewsets.ModelViewSet):
    # TODO: Filter foods based on sent date and foods date
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
