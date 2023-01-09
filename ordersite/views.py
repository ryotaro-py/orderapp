from django.shortcuts import redirect
from django.views import generic
from .models import Drink, Detail
from .forms import DrinkForm
from .graph import plot_graph
from datetime import datetime, timezone, timedelta


class ToppageView(generic.TemplateView):
    template_name = "ordersite/toppage.html"


class OrderView(generic.TemplateView):
    template_name = "ordersite/order.html"

    def get_context_data(self):
        context = super().get_context_data()
        drinks = Drink.objects.filter(status=True)
        context["drinks"] = drinks
        weight = 0.5
        JST = timezone(timedelta(hours=9), "JST")
        drink_to_order_list = []
        for drink in drinks:
            drink_amounts = Detail.objects.filter(name=drink).order_by("-created_at")
            if drink_amounts.count() >= 2:
                n = 0
                average = timedelta(0)
                while n <= drink_amounts.count() - 2:
                    difference = (
                        drink_amounts[n].created_at - drink_amounts[n + 1].created_at
                    )
                    average += difference * (weight**n)
                    n += 1
                average = (1 - weight) * average
                latest_drink = drink_amounts[0]
                between_today_latest = datetime.now(JST) - latest_drink.created_at

                if between_today_latest >= average:
                    drink_to_order_list.append([drink, latest_drink])
        context["drink_to_order"] = drink_to_order_list
        return context


class OrderfixView(generic.TemplateView):
    template_name = "ordersite/orderfix.html"

    def post(self, request):
        drink_id_list = self.request.POST.getlist("drink_id")
        drink_count_list = self.request.POST.getlist("drink_count")
        drink_amount = Drink.objects.all().count()
        if len(drink_id_list) == len(drink_count_list) == drink_amount:
            i = 0
            for drink_id in drink_id_list:
                drink = Drink.objects.get(id=drink_id)
                drink_create = Detail.objects.create(
                    name=drink, count=int(drink_count_list[i])
                )
                i += 1
        return redirect("orderfix")

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        drinks = Drink.objects.all()
        order_list = []
        for drink in drinks:
            detail = Detail.objects.filter(name=drink).order_by("-created_at").first()
            order_list.append([drink.name, detail.count])
        context["order_list"] = order_list
        return context


class DataTopView(generic.TemplateView):
    template_name = "ordersite/datatop.html"


class DataAmountView(generic.ListView):
    template_name = "ordersite/dataamount.html"
    queryset = Drink.objects.filter(status=True)
    paginate_by = 10


class DataAmountDetailView(generic.TemplateView):
    template_name = "ordersite/dataamountdetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        drink = Drink.objects.get(id=self.kwargs["drink_id"])
        drink_amounts = Detail.objects.filter(name=drink)
        this_month = datetime.now().month
        this_year = datetime.now().year
        month = this_month
        year = this_year
        this_month_drink_amounts = drink_amounts.filter(
            created_at__month=this_month, created_at__year=this_year
        )
        this_month_drink_counts = 0
        for this_month_drink_amount in this_month_drink_amounts:
            this_month_drink_counts += this_month_drink_amount.count
        drink_amounts_list = [[this_month, this_month_drink_counts]]
        for i in range(11):
            if month - 1 == 0:
                month = 12
                year -= 1
                month_drink_amounts = drink_amounts.filter(
                    created_at__month=month, created_at__year=year
                )
                drink_counts = 0
                for month_drink_amount in month_drink_amounts:
                    drink_counts += month_drink_amount.count
                drink_amounts_list.append([month, drink_counts])
            else:
                month -= 1
                month_drink_amounts = drink_amounts.filter(
                    created_at__month=month, created_at__year=year
                )
                drink_counts = 0
                for month_drink_amount in month_drink_amounts:
                    drink_counts += month_drink_amount.count
                drink_amounts_list.append([month, drink_counts])
        drink_amounts_list.reverse()
        x = [str(x[0]) for x in drink_amounts_list]
        y = [y[1] for y in drink_amounts_list]
        title = "data"
        ylabel = "number of orders"
        chart = plot_graph(x, y, title, x, ylabel)
        context["chart"] = chart
        context["drink"] = drink
        return context


class DataPriceView(generic.ListView):
    template_name = "ordersite/dataprice.html"
    queryset = Drink.objects.filter(status=True)
    paginate_by = 10


class DataPriceDetailView(generic.TemplateView):
    template_name = "ordersite/datapricedetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        drink = Drink.objects.get(id=self.kwargs["drink_id"])
        drink_amounts = Detail.objects.filter(name=drink).order_by("created_at")
        price = drink.price
        this_month = datetime.now().month
        this_year = datetime.now().year
        month = this_month
        year = this_year
        this_month_drink_amounts = drink_amounts.filter(
            created_at__month=this_month, created_at__year=this_year
        )
        this_month_drink_counts = 0
        for this_month_drink_amount in this_month_drink_amounts:
            this_month_drink_counts += this_month_drink_amount.count
        this_month_drink_price = this_month_drink_counts * price
        drink_amounts_list = [[this_month, this_month_drink_price]]
        for i in range(11):
            if month - 1 == 0:
                month = 12
                year -= 1
                month_drink_amounts = drink_amounts.filter(
                    created_at__month=month, created_at__year=year
                )
                drink_counts = 0
                for month_drink_amount in month_drink_amounts:
                    drink_counts += month_drink_amount.count
                drink_price = drink_counts * price
                drink_amounts_list.append([month, drink_price])
            else:
                month -= 1
                month_drink_amounts = drink_amounts.filter(
                    created_at__month=month, created_at__year=year
                )
                drink_counts = 0
                for month_drink_amount in month_drink_amounts:
                    drink_counts += month_drink_amount.count
                drink_price = drink_counts * price
                drink_amounts_list.append([month, drink_price])
        drink_amounts_list.reverse()
        x = [str(x[0]) for x in drink_amounts_list]
        y = [y[1] for y in drink_amounts_list]
        title = "price"
        ylabel = "total amount"
        chart = plot_graph(x, y, title, x, ylabel)
        context["chart"] = chart
        context["drink"] = drink
        return context


class TodayOrderView(generic.TemplateView):
    template_name = "ordersite/todayorder.html"

    def get_context_data(self):
        context = super().get_context_data()
        JST = timezone(timedelta(hours=9), "JST")
        today_drink_list = []
        drinks = Drink.objects.all()
        today = datetime(
            datetime.now(JST).year, datetime.now(JST).month, datetime.now(JST).day
        )
        for drink in drinks:
            details = Detail.objects.filter(name=drink, created_at__gte=today)
            count = 0
            if details.exists():
                for detail in details:
                    count += detail.count
                if count != 0:
                    today_drink_list.append([drink, count])
        context["list"] = today_drink_list
        return context


class RegisterDeleteView(generic.FormView):
    template_name = "ordersite/register.html"
    form_class = DrinkForm

    def get_context_data(self):
        context = super().get_context_data()
        return context

    def form_valid(self, form):
        form.save()
        return redirect("registerdone")


class RegisterDoneView(generic.TemplateView):
    template_name = "ordersite/registerdone.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["drink"] = Drink.objects.last()
        return context


class DeleteView(generic.TemplateView):
    template_name = "ordersite/delete.html"

    def get_context_data(self):
        context = super().get_context_data()
        drinks = Drink.objects.filter(status=True)
        context["drinks"] = drinks
        return context

    def post(self, request):
        drink_id = self.request.POST["drink_id"]
        delete_drink = Drink.objects.get(id=drink_id)
        delete_drink.status = False
        delete_drink.save()
        return redirect("delete")


class ReviveView(generic.TemplateView):
    template_name = "ordersite/revival.html"

    def get_context_data(self):
        context = super().get_context_data()
        delete_drinks = Drink.objects.filter(status=False)
        context["drinks"] = delete_drinks
        return context

    def post(self, request):
        drink_id = self.request.POST["drink_id"]
        delete_drink = Drink.objects.get(id=drink_id)
        delete_drink.status = True
        delete_drink.save()
        return redirect("revival")
