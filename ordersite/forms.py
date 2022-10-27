from cProfile import label
from dataclasses import field
from django import forms
from .models import Drink, Detail

class DrinkForm(forms.ModelForm):

    class Meta:
        model = Drink
        fields = ("name",)
        labels ={"name":"名前",}

class DetailForm(forms.ModelForm):

    class Meta:
        model = Detail
        fields = ("price",)
        labels = {"price":"値段",}