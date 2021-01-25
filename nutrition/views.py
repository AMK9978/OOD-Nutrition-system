import base64
import datetime
import json

import grpc
import jwt
import requests
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

import auth_pb2_grpc
from nutrition.models import Food, FoodReserve, User
from nutrition.serializers import FoodReserveSerializer, FoodSerializer, UserSerializer

CACHE_TTL = 60 * 2
PUBLIC_KEY = base64.b64decode(
    "LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlHYk1CQUdCeXFHU000OUFnRUdCU3VCQkFBakE0R0dBQVFBdmRrYTFzcTBRd2h0QStieDFBVHVTSUEzT2oxOQpYMk0rVExzZDF3SlBGbTI0U05OUXFUWFBidFFLamhFemhsK2ZDNWExZ2ttRzNpaTJBcWt6MnRaTWUzVUFDb3JSCm1QZXh5blR0cFFSQWFKalhDOGpkRXNDU3UvMlMrblpBMmdBc25uNDBRQWxzaEpBZHMybmRYd1FBSjk5T2tXeTUKcEduRkQ2M042Vy84ODlZQW9acz0KLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0t")
SECRET_KEY = "LS0tLS1CRUdJTiBFQyBQUklWQVRFIEtFWS0tLS0tCk1JSGNBZ0VCQkVJQktIMVhZWG5MalZOS0FBRUZVbGVCV1FQcVpWRWdXdkdBcHc3bm40cWpwRStFTVVjNGEzblEKcE5GZVk3RXM5dDFqTks0OE1DcnhCTXU4MDNvRnUzdEIrd3lnQndZRks0RUVBQ09oZ1lrRGdZWUFCQUM5MlJyVwp5clJEQ0cwRDV2SFVCTzVJZ0RjNlBYMWZZejVNdXgzWEFrOFdiYmhJMDFDcE5jOXUxQXFPRVRPR1g1OExscldDClNZYmVLTFlDcVRQYTFreDdkUUFLaXRHWTk3SEtkTzJsQkVCb21OY0x5TjBTd0pLNy9aTDZka0RhQUN5ZWZqUkEKQ1d5RWtCMnphZDFmQkFBbjMwNlJiTG1rYWNVUHJjM3BiL3p6MWdDaG13PT0KLS0tLS1FTkQgRUMgUFJJVkFURSBLRVktLS0tLQ===="


def decode(user_token: str):
    print(user_token)
    print(PUBLIC_KEY)
    decoded_token = jwt.decode(user_token, PUBLIC_KEY, algorithms='ES512', options={"verify_signature": False})
    print(decoded_token)
    print(decoded_token['username'])


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
        decode(str(request.headers.get('Authorization')).split(" ")[1])
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


class Login(viewsets.ModelViewSet):
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
