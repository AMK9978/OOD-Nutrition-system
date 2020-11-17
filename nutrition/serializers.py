# serializers.py
from rest_framework import serializers

from .models import User, Food


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'charge', 'is_chef')


class FoodSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Food
        fields = ('id', 'name', 'price')
