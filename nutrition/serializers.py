from rest_framework import serializers
from rest_framework import fields
from nutrition.models import Food, User, FoodReserve

class UserSerializer(serializers.ModelSerializer):
    foods_reserved = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'charge', 'is_chef', 'foods_reserved']

class FoodSerializer(serializers.ModelSerializer):
    reserved = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Food
        fields = ['name', 'price', 'capacity', 'pub_date', 'reserved']

class FoodReserveSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FoodReserve
        fields = ['date', 'user_id', 'food_id']