# Create your models here.

from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    name = models.CharField(default='Amir', max_length=48)
    charge = models.IntegerField(default=0)
    is_chef = models.BooleanField(default=False)


class Food(models.Model):
    name = models.CharField(max_length=48)
    price = models.IntegerField(default=0)
    meal_choices = [
        ('b', 'breakfast'),
        ('l', 'launch'),
        ('d', 'dinner'),
    ]
    meal = models.CharField(default="launch", choices=meal_choices, max_length=16)
    capacity = models.IntegerField(default=0)
    pub_date = models.DateField('date published')

    def __str__(self):
        return "{}-{}".format(self.name, self.pub_date)


class FoodReserve(models.Model):
    date = models.DateField(default=datetime.now().date())
    user_id = models.ForeignKey(User, related_name="foods_reserved", on_delete=models.CASCADE)
    food_id = models.ForeignKey(Food, related_name="reserved", on_delete=models.CASCADE)

    def __str__(self):
        return "{}-{}-{}".format(self.user_id, self.food_id, self.date)
