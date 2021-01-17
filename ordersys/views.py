from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.http import HttpResponseRedirect
from django.conf import settings

from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.http import is_safe_url

from .models import Order, Product, ProductAmount, TempOrder
from .forms import OrderCreationForm, LogInForm

class OrdersView(LoginRequiredMixin, generic.ListView):
    login_url = '/ordersys/login/'
    model=Order
    template_name = 'ordersys/orders.html'
    context_object_name = 'orders_list'
    orderint = ['id']
    
    def get_queryset(self):
        return Order.objects.all()


class PendingOrdersView(OrdersView):
    def get_queryset(self):
        return Order.objects.filter(status='Pending').all()

class PrepareOrdersView(OrdersView):
    def get_queryset(self):
        return Order.objects.filter(status='Prepare').all()

class CollectOrdersView(OrdersView):
    def get_queryset(self):
        return Order.objects.filter(status='Collect').all()

class DoneOrdersView(OrdersView):
    def get_queryset(self):
        return Order.objects.filter(status='Done').all()

class FailedOrdersView(OrdersView):
    def get_queryset(self):
        return Order.objects.filter(status='Error').all()

class CustomersOrdersView(generic.ListView):
    login_url = '/ordersys/login/'
    model=Order    
    template_name = 'ordersys/customers.html'
    context_object_name = 'orders_list'
    orderint = ['id']

    def get_queryset(self):
        return Order.objects.exclude(status='Done').all()

class LogView(auth_views.LoginView):
    template_name = 'ordersys/login.html'
    model = LogInForm

    fields = ['username', 'password']
    def get(self, request):
        context = {
            'login_form': LogInForm(),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        login_data = LogInForm(request.POST)
        if login_data.is_valid():    
            username = login_data.cleaned_data['username']
            password = login_data.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                redirect = request.GET.get('next', '')
                if is_safe_url(url=redirect, allowed_hosts=settings.ALLOWED_HOSTS):
                    return HttpResponseRedirect(redirect)
                else:
                    return HttpResponseRedirect(reverse('ordersys:customers'))
            else:
                return HttpResponseRedirect(reverse('ordersys:login'))

class ManagerMenuView(LoginRequiredMixin, generic.CreateView):
    login_url = '/ordersys/login/'
    template_name = 'ordersys/manager_tab.html'
    
    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        if request.POST.get("Daily"):
            return render(request, 'ordersys/daily_report.html')
        if request.POST.get("Monthly"):
            return render(request, 'ordersys/monthly_report.html')
        if request.POST.get("Annual"):
            return render(request, 'ordersys/annual_report.html')
        if request.POST.get("Workers"):
            return render(request, 'ordersys/manage_workers.html')
        if request.POST.get("Orders"):
            return render(request, 'ordersys/manage_orders.html')   
        if request.POST.get("Stock"):
            return render(request, 'ordersys/manage_stock.html')         
class CreateOrderView(LoginRequiredMixin, generic.CreateView):
    login_url = '/ordersys/login/'
    template_name = 'ordersys/create_order.html'
    model = OrderCreationForm

    fields = ['product', 'amount']

    def get(self, request):
        context = {
            'creation_form': OrderCreationForm(), 
            'temp_order': TempOrder.objects.all(),
            }
        return render(request, self.template_name, context)
    
    def post(self, request):
        order_creation_data = OrderCreationForm(request.POST)
        if order_creation_data.is_valid():
            product = order_creation_data.cleaned_data['product']
            amount = order_creation_data.cleaned_data['amount']
            deletion = order_creation_data.cleaned_data['to_delete']
            if request.POST.get("Add"):
                self.add_to_order(product, amount)
            elif request.POST.get("Finish"):
                self.finish_order()
            elif request.POST.get("Delete"):
                TempOrder.objects.all().delete()
            elif request.POST.get("Delete Item"):
                self.delete_from_order(deletion)
        return HttpResponseRedirect(reverse('ordersys:create'))

    def add_to_order(self, product, amount):
        try:
            product_on_temp = TempOrder.objects.get(product=product)
            if product_on_temp:
                if product_on_temp.amount_of_product + amount > 0:
                    product_on_temp.amount_of_product += amount
                    product_on_temp.save()
        except:    
            if product != None and amount!= None and amount > 0:
                temp_order = TempOrder(
                    product=product, 
                    amount_of_product=amount
                    )
                temp_order.save()

    def finish_order(self):
        if TempOrder.objects.all():
            order = Order()
            order.save()
            order = Order.objects.last()
            for temp_item in TempOrder.objects.all():
                product_amount = ProductAmount(
                    order=order, 
                    product=temp_item.product, 
                    amount_of_product=temp_item.amount_of_product
                    )
                product_amount.save()
            TempOrder.objects.all().delete()
    
    def delete_from_order(self, to_delete):
        if to_delete != None:
            TempOrder.objects.get(product=to_delete).delete()

def start_preparing_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    order.status = "Prepare"
    order.save()
    return HttpResponseRedirect(reverse('ordersys:pending'))

def finish_preparing_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    order.status = "Collect"
    order.save()
    return HttpResponseRedirect(reverse('ordersys:prepare'))

def collected_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    order.status = "Done"
    order.save()
    return HttpResponseRedirect(reverse('ordersys:collect'))