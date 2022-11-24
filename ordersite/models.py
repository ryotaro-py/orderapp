from email.policy import default
from django.db import models
from datetime import datetime




class Drink(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.IntegerField()
    status = models.BooleanField(default=True)

class Detail(models.Model):
    name = models.ForeignKey(Drink, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=datetime.now)
    



