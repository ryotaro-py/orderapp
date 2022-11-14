from django.shortcuts import redirect
from django.views import generic
from .models import Drink, Detail
from .forms import DrinkForm, DetailForm
from .graph import plot_graph
from datetime import datetime, timezone, timedelta




class ToppageView(generic.TemplateView):
    template_name = "ordersite/toppage.html"

class OrderView(generic.TemplateView):
    template_name = "ordersite/order.html"

    def get_context_data(self):
        context = super().get_context_data()
        drinks= Drink.objects.all()
        context['drinks'] = drinks
        # 予測機能について
        JST = timezone(timedelta(hours=9), "JST")
        drink_to_order_list = []
        for drink in drinks:
            drink_amounts = Detail.objects.filter(name=drink).order_by('-created_at')    
            if drink_amounts.count() >= 2:
                latest_drink = drink_amounts[0]
                second_latest_drink = drink_amounts[1]
                s = latest_drink.created_at - second_latest_drink.created_at
                t = datetime.now(JST) - latest_drink.created_at
                if t >= s:
                    drink_to_order_list.append([drink, latest_drink])
        context['drink_to_order'] = drink_to_order_list
        return context

class OrderfixView(generic.TemplateView):
    template_name = "ordersite/orderfix.html"

    def post(self, request):
        drink_id_list = self.request.POST.getlist('drink_id')
        drink_count_list = self.request.POST.getlist('drink_count')
        drink_amount = Drink.objects.all().count()
        if len(drink_id_list)==len(drink_count_list)==drink_amount:
            i = 0
            for drink_id in drink_id_list:
                drink = Drink.objects.get(id=drink_id)
                drink_create = Detail.objects.create(name=drink, count=int(drink_count_list[i]))
                i += 1
        return redirect('orderfix')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        drinks = Drink.objects.all()
        order_list = []
        for drink in drinks:
            detail = Detail.objects.filter(name=drink).order_by('-created_at').first()
            order_list.append([drink.name, detail.count])
        context['order_list'] = order_list
        return context

class DataTopView(generic.TemplateView):
    template_name = "ordersite/datatop.html"

class DataAmountView(generic.ListView):
    template_name = "ordersite/dataamount.html"
    model = Drink
    paginate_by = 10

class DataAmountDetailView(generic.TemplateView):
    template_name = "ordersite/dataamountdetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #drinkの詳細情報が作成順になって取得
        drink = Drink.objects.get(id=self.kwargs['drink_id'])
        drink_amounts = Detail.objects.filter(name=drink).order_by('-created_at')
        
        #同じ日に2回以上注文していた場合、monthとdrink_amountがずれる
        #もし、同じ日に二つ以上のデータがはいっているのなら、その分カウントを追加する。
        counts = drink_amounts.count()
        month = datetime.now().month
        #yearが変わる場合はif文で精査する
        year = datetime.now().year

        i = 0
        amounts_list = []
        while  i <= counts:
            drink_amount = drink_amounts.filter(created_at__month=month)
            count = 0
            for amount in drink_amount:
                count += amount.count
            amounts_list.append([month,count])
            month -= 1
            i += 1
        amounts_list.reverse()
        x = [x[0] for x in amounts_list]
        y = [y[1] for y in amounts_list]
        title = 'data'
        ylabel = 'number of orders'
        chart = plot_graph(x,y,title,ylabel)
        context['chart'] = chart
        context['drink'] = drink
        print(amounts_list)
        return context

class DataPriceView(generic.ListView):
    template_name = "ordersite/dataprice.html"
    model = Drink
    paginate_by = 5

class DataPriceDetailView(generic.TemplateView):
    template_name = "ordersite/datapricedetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        drink = Drink.objects.get(id=self.kwargs['drink_id'])
        drink_amounts = Detail.objects.filter(name=drink).order_by('created_at')
        price = drink_amounts.first().price
        counts = drink_amounts.count()
        month = datetime.now().month
        #yearが変わる場合はif文で精査する
        i = 0
        amounts_list = []
        while  i <= counts:
            drink_amount = drink_amounts.filter(created_at__month=month)
            count = 0
            for amount in drink_amount:
                count += amount.count
            amounts_list.append([month,count*price])
            month -= 1
            i += 1
        amounts_list.reverse()
        x = [x[0] for x in amounts_list]
        y = [y[1] for y in amounts_list]
        title = 'price'
        ylabel = 'total amount'
        chart = plot_graph(x,y,title,ylabel)
        context['chart'] = chart
        context['drink'] = drink
        print(amounts_list)
        return context

class TodayOrderView(generic.TemplateView):
    template_name = "ordersite/todayorder.html"

    def get_context_data(self):
        context = super().get_context_data()
        year = datetime.now().year
        month = datetime.now().month
        day = datetime.now().day
        details = Detail.objects.filter(created_at__year=year).filter(created_at__month=month).filter(created_at__day=day)
        count = 0
        today_drink_list = []
        drinks = Drink.objects.all()
        for drink in drinks:
            if details.filter(name=drink).exists():
                for detail in details.filter(name=drink):
                    drink = detail.name.name
                    count += detail.count
                today_drink_list.append([drink, count])
        context['list'] = today_drink_list
        return context

class RegisterView(generic.FormView):
    template_name= "ordersite/register.html"
    form_class = DrinkForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drink_id'] = Drink.objects.all().last().id
        return context

    def form_valid(self, form):
        form.save()
        drink_id = int(self.request.POST['drink_id'])
        return redirect('registerdetail', pk=drink_id+1)

class RegisterDetailView(generic.FormView):
    template_name = "ordersite/registerdetail.html"
    form_class = DetailForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drink'] = Drink.objects.get(id=self.kwargs['pk']).name
        return context

    def form_valid(self, form):
        detail = form.save(commit=False)
        detail.name = Drink.objects.get(id=self.kwargs['pk'])
        detail.save()
        return redirect('toppage')


    



