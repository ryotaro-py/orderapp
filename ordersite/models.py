from email.policy import default
from enum import auto
from time import timezone
from turtle import update
from django.db import models
from datetime import datetime

class Drink(models.Model):
    name = models.CharField(max_length=100)

class Detail(models.Model):
    name = models.ForeignKey(Drink, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(auto_now=True)



