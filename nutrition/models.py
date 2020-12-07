# Create your models here.
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


# Create your models here.
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(),
                          editable=False)
    charge = models.IntegerField
    is_chef = models.BooleanField(default=False)


class Food(models.Model):
    name = models.CharField(max_length=48)
    price = models.IntegerField(default=0)
    capacity = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published',default=datetime.today())


class FoodReserve(models.Model):
    date = models.DateTimeField(default=datetime.today())
    user_id = models.ForeignKey(User, related_name="foods_reserved", on_delete=models.CASCADE)
    food_id = models.ForeignKey(Food, related_name="reserved", on_delete=models.CASCADE)
