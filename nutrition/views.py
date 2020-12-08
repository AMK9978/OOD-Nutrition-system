from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.fields import JSONField

from nutrition.models import Food, FoodReserve, User
from nutrition.serializers import FoodReserveSerializer, FoodSerializer, UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer


class FoodReserveViewSet(viewsets.ModelViewSet):
    queryset = FoodReserve.objects.all()
    serializer_class = FoodReserveSerializer

    def perform_create(self, serializer):
        body_unicode = self.request.body.decode('utf-8')
        body = JSONField.loads(body_unicode)
        my_user = body['user_id']
        my_food = body['food_id']
        if my_user.charge < my_food.price:
            raise ValidationError('not enough charge')
        my_user.chaege -= my_food.price
        serializer.save(self.request.data)
