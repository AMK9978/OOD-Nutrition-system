import datetime

import requests
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from nutrition.models import Food, FoodReserve, User
from nutrition.serializers import FoodReserveSerializer, FoodSerializer, UserSerializer
from .Payment import PaymentGatewayAdapter


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

    def list(self, request, *args, **kwargs):
        tomorrow = datetime.datetime.today().date() + datetime.timedelta(days=1)
        next_week = datetime.datetime.today().date() + datetime.timedelta(days=7)
        return Response(list(Food.objects.filter(pub_date__range=[tomorrow, next_week]).values()))


class FoodReserveViewSet(viewsets.ModelViewSet):
    queryset = FoodReserve.objects.all()
    serializer_class = FoodReserveSerializer

    def retrieve(self, request, *args, **kwargs):
        return Response(list(FoodReserve.objects.filter(user_id_id=kwargs["pk"]).values()))

    def perform_create(self, serializer):
        my_user = self.request.data['user_id']
        my_food = self.request.data['food_id']
        user = User.objects.get(id=my_user)
        food = Food.objects.get(id=my_food)
        print(self.request.headers.get('Authorization'))
        today_date = datetime.datetime.today().date()
        if today_date > food.pub_date:
            raise ValidationError('Invalid food to be reserved')
        if user.charge < food.price:
            raise ValidationError('not enough charge')
        if food.capacity <= 0:
            raise ValidationError('not enough food is left')
        food_reserved = FoodReserve.objects.filter(user_id_id=user.id, date=food.pub_date).last()
        if food_reserved is not None:
            raise ValidationError("You've already reserved food this day")
        user.charge -= food.price
        food.capacity -= 1
        user.save()
        food.save()
        serializer.save()


class Auth(viewsets.ModelViewSet):
    def retrieve(self, request, *args, **kwargs):
        # Send request to auth server and return token to user
        response = requests.post("127.0.0.1:50051",
                                 {"username": request.data['username'], "password": request.data['password']})

        return response


class Charge(viewsets.ModelViewSet):
    def retrieve(self, request, *args, **kwargs):
        return PaymentGatewayAdapter().sep_request_token(request.data['amount'], 0,
                                                         ['https://google.com', 'https://google.com'])
