import datetime
import json

import grpc
import requests
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

import auth_pb2_grpc
from nutrition.models import Food, FoodReserve
from nutrition.serializers import FoodReserveSerializer, FoodSerializer, UserSerializer

CACHE_TTL = 60 * 2


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    def retrieve(self, request, *args, **kwargs):
        serializer_class = UserSerializer(request.user)
        return JsonResponse(serializer_class.data, status=200)


class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

    @method_decorator(cache_page(CACHE_TTL))
    def list(self, request, *args, **kwargs):
        tomorrow = datetime.datetime.today().date() + datetime.timedelta(days=1)
        next_week = datetime.datetime.today().date() + datetime.timedelta(days=7)
        return Response(list(Food.objects.filter(pub_date__range=[tomorrow, next_week]).values()))


class FoodReserveViewSet(APIView):
    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request):
        return Response(list(FoodReserve.objects.filter(user_id_id=request.user.id).values()))

    @csrf_exempt
    def post(self, request):
        user = self.request.user
        my_food = self.request.data['food_id']
        food = Food.objects.get(id=my_food)
        print(user.name)
        today_date = datetime.datetime.today().date()
        if today_date > food.pub_date:
            raise ValidationError('Invalid food to be reserved')
        if user.charge < food.price:
            raise ValidationError('not enough charge')
        if food.capacity <= 0:
            raise ValidationError('not enough food is left')
        food_reserved = FoodReserve.objects.filter(user_id_id=user.id, date=food.pub_date).last()
        if food_reserved is not None:
            raise ValidationError("You've already reserved food this day {}".format(food_reserved))
        user.charge -= food.price
        food.capacity -= 1
        user.save()
        food.save()
        serializer = FoodReserveSerializer(data={"food_id": food.id, "user_id": user.id})
        serializer.is_valid(raise_exception=ValidationError, )
        serializer.save()
        return JsonResponse(serializer.data, status=200, safe=False)


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


class Login(viewsets.ModelViewSet):
    permission_classes = []

    def retrieve(self, request, *args, **kwargs):
        # TODO: Use gRPC calls instead of http calls which are being used currently:
        channel = grpc.insecure_channel('localhost:50051')
        stub = auth_pb2_grpc.AuthStub(channel)
        import auth_pb2
        try:
            msg = str(stub.Login(
                request=auth_pb2.Credentials(username=request.data["username"], password=request.data["password"])))
        except:
            return JsonResponse({"msg": "Incorrect username or password"}, status=400)
        import re
        l = list(re.findall("\".*\"", msg))
        dic = {"token": l[0][1:-1], "refresh": l[1][1:-1]}
        print(l[0], '\n')
        print(l[1], '\n')
        channel.close()
        return JsonResponse(dic, status=200, safe=False)


class Charge(viewsets.ModelViewSet):
    def retrieve(self, request, *args, **kwargs):
        return JsonResponse({"msg": "Comming soon!"}, status=200)
