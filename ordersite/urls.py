from django.urls import path
from . import views

urlpatterns = [
    path('',views.ToppageView.as_view() , name='toppage'),
    path('order', views.OrderView.as_view(), name='order'),
    path('orderfix', views.OrderfixView.as_view(), name='orderfix'),
]