# Create your models here.
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(),
                          editable=False)
    name = models.CharField(default='Amir', max_length=48)
    charge = models.IntegerField
    is_chef = models.BooleanField(default=False)


class Food(models.Model):
    name = models.CharField(max_length=48)
    price = models.IntegerField(default=0)
    capacity = models.IntegerField(default=0)
    pub_date = models.DateField('date published')


class FoodReserve(models.Model):
    date = models.DateTimeField
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    food_id = models.ForeignKey(Food, on_delete=models.CASCADE)
