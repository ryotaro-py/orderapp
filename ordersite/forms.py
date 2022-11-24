from cProfile import label
from dataclasses import field
from django import forms
from .models import Drink, Detail

class DrinkForm(forms.ModelForm):

    class Meta:
        model = Drink
        fields = ("name","price",)
        labels ={"name":"名前", "price":"金額",}

