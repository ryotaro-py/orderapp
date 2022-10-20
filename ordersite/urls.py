from django.urls import path
from . import views

urlpatterns = [
    path('',views.ToppageView.as_view() , name='toppage'),
    path('order', views.OrderView.as_view(), name='order'),
    path('orderfix', views.OrderfixView.as_view(), name='orderfix'),
    path('data', views.DataTopView.as_view(), name='data'),
    path('data/amount', views.DataAmountDetailView.as_view(), name='dataamount'),
    path('data/amount/<int:drink_id>', views.DataAmountDetailView.as_view(), name='dataamountdetail'),
    path('data/amount/<int:drink_id>/plot', views.get_svg, name='amountplot'),
    path('data/price', views.DataPriceView.as_view(), name='dataprice'),
    path('data/price/<int:drink_id>', views.DataPriceDetailView.as_view(), name='datapricedetail'),
    path('data/price/<int:drink_id>/plot', views.get_svg, name='priceplot'),
]