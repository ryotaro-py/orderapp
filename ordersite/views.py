from multiprocessing import context
from django.shortcuts import render, redirect
from django.views import generic
from .models import Drink, Detail

class ToppageView(generic.TemplateView):
    template_name = "ordersite/toppage.html"

class OrderView(generic.TemplateView):
    template_name = "ordersite/order.html"

    def get_context_data(self):
        context = super().get_context_data()
        drinks= Drink.objects.all()
        # drink_amount = drinks.count()
        # drink_list = []
        # for drink in drinks:
        #     drink_list.append([drink,])
        context['drinks'] = drinks    
        return context

    def post(self, request):
        drink_id = self.request.POST.getlist('drink_id')
        drink_count = self.request.POST.getlist('drink_count')
        print(drink_id, drink_count)
        drink_amount = Drink.objects.all().count()
        print(drink_amount)
        return redirect('orderfix')



class OrderfixView(generic.TemplateView):
    template_name = "ordersite/orderfix.html"

    def post(self, request):
        drink_id = self.request.POST.getlist('drink_id')
        drink_count = self.request.POST.getlist('drink_count')
        drink_amount = Drink.objects.all().count()
        print(drink_id, drink_count)
        return redirect('orderfix')

