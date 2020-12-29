import datetime
import json

import requests
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from nutrition.models import Food, FoodReserve, User
from nutrition.serializers import FoodReserveSerializer, FoodSerializer, UserSerializer
from .Payment import PaymentGatewayAdapter

CACHE_TTL = 60 * 2


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

    @method_decorator(cache_page(CACHE_TTL))
    def list(self, request, *args, **kwargs):
        tomorrow = datetime.datetime.today().date() + datetime.timedelta(days=1)
        next_week = datetime.datetime.today().date() + datetime.timedelta(days=7)
        return Response(list(Food.objects.filter(pub_date__range=[tomorrow, next_week]).values()))


class FoodReserveViewSet(viewsets.ModelViewSet):
    queryset = FoodReserve.objects.all()
    serializer_class = FoodReserveSerializer

    @method_decorator(cache_page(CACHE_TTL))
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


class AdminLogin(viewsets.ModelViewSet):
    def retrieve(self, request, *args, **kwargs):
        env_file = open('../.env', 'r')
        username = ""
        password = ""
        for line in env_file.readlines():
            if line.startswith("ADMIN_USER="):
                username = line.split("ADMIN_USER=")[1].strip()
            elif line.startswith("ADMIN_PASS="):
                password = line.split("ADMIN_PASS=")[1].strip()
        env_file.close()
        print(username)
        print(password)
        url = "http://localhost:9090/login"

        payload = "{\n  \"username\":\"" + username + "\", \n  \"password\":\"" + password + "\"\n}"
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        result = json.loads(response.text)
        refresh = result["refresh"]["token"]
        access = result["access"]["token"]
        admin_file = open("../.admin_file", 'w')
        admin_file.write("access:{}".format(access))
        admin_file.write("\n")
        admin_file.write("refresh:{}".format(refresh))
        admin_file.close()
        return response


def read_admin_file():
    admin_file = open('../.admin_file', 'r')
    access = ""
    refresh = ""
    for r in admin_file.readlines():
        if r.startswith("access:"):
            access = r.split("access:")[1]
        elif r.startswith("refresh:"):
            refresh = r.split("refresh:")[1]
    return access, refresh


class Signup(viewsets.ModelViewSet):
    def retrieve(self, request, *args, **kwargs):
        url = "http://localhost:9090/signup"
        access, refresh = read_admin_file()

        if access == "":
            AdminLogin.as_view()
            access, refresh = read_admin_file()

        payload = "{\n  \"username\":\"" + request['username'] + "\", \n  \"password\":\"" + request[
            'password'] + "\"\n}"
        headers = {
            'Authorization': 'Bearer {}'.format(access),
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return response


class Login(viewsets.ModelViewSet):
    def retrieve(self, request, *args, **kwargs):
        # Send request to auth server and return token to user
        url = "http://localhost:9090/login"

        payload = "{\n  \"username\":\"" + request['username'] + "\", \n  \"password\":\"" + request['password'] + "\"\n}"
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response


class Charge(viewsets.ModelViewSet):
    def retrieve(self, request, *args, **kwargs):
        return PaymentGatewayAdapter().sep_request_token(request.data['amount'], 0,
                                                         ['https://google.com', 'https://google.com'])
