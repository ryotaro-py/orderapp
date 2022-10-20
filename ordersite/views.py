from multiprocessing import context
from django.shortcuts import render, redirect
from django.views import generic
from django.http import HttpResponse
from .models import Drink, Detail
import datetime
import io
import matplotlib.pyplot as plt
import numpy as np


class ToppageView(generic.TemplateView):
    template_name = "ordersite/toppage.html"

class OrderView(generic.TemplateView):
    template_name = "ordersite/order.html"

    def get_context_data(self):
        context = super().get_context_data()
        drinks= Drink.objects.all()
        context['drinks'] = drinks    
        return context

class OrderfixView(generic.TemplateView):
    template_name = "ordersite/orderfix.html"

    def post(self, request):
        drink_id_list = self.request.POST.getlist('drink_id')
        drink_count_list = self.request.POST.getlist('drink_count')
        drink_amount = Drink.objects.all().count()
        print(drink_id_list, drink_count_list)
        print(drink_amount)
        if len(drink_id_list)==len(drink_count_list)==drink_amount:
            i = 0
            for drink_id in drink_id_list:
                drink = Drink.objects.get(id=drink_id)
                drink_name = Detail.objects.get(name=drink)
                print(drink_name)
                print(type(drink_name.count), type(drink_count_list[0]))
                drink_name.count += int(drink_count_list[i])
                print(drink_count_list[i])
                i += 1
                print(drink_name.count)
                drink_name.save()
        return redirect('orderfix')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        details = Detail.objects.all()
        order_list = []
        for detail in details:
            drink = detail.name
            print(drink, type(drink))
            order_list.append([drink,detail.count])
        print(order_list)
        context['order_list'] = order_list
        return context

class DataTopView(generic.TemplateView):
    template_name = "ordersite/datatop.html"

class DataAmountView(generic.ListView):
    tamplate_name = "ordersite/dataamount.html"
    model = Drink
    paginate_by = 20

class DataAmountDetailView(generic.TemplateView):
    template_name = "ordersite/dataamountdetail.html"

def setPlt(drink_id):

class DataPriceView(generic.TemplateView):
    template_name = "ordresite/dataprice.html"

class DataPriceDetailView(generic.TemplateView):
    template_name = "ordersite/datapricedetail.html"