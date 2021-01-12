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

class OrdersView(generic.ListView):
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

class CustomersOrdersView(OrdersView):
    template_name = 'ordersys/customers.html'

    def get_queryset(self):
        return Order.objects.exclude(status='Done').all()

class LogView(auth_views.LoginView):
    template_name = 'ordersys/login.html'
    model = LogInForm

    fields = ['username', 'password']
    def get(self, request):
        context = {
            'form': LogInForm(),
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
                    return cHttpResponseRedirect(reverse('ordersys:customers'))
            else:
                return HttpResponseRedirect(reverse('ordersys:login'))

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

            if request.POST.get("Add"):
                product = order_creation_data.cleaned_data['product']
                amount = order_creation_data.cleaned_data['amount']
                try:
                    product_on_temp = TempOrder.objects.get(product=product)
                    if product_on_temp:
                        if product_on_temp.amount_of_product + amount > 0:
                            product_on_temp.amount_of_product += amount
                            product_on_temp.save()
                except:    
                    if product != None and amount!= None and amount > 0:
                        temp_order = TempOrder(product=product, amount_of_product=amount)
                        temp_order.save()

            elif request.POST.get("Finish"):
                if TempOrder.objects.all():
                    order = Order()
                    order.save()
                    order = Order.objects.last()
                    for temp_item in TempOrder.objects.all():
                        product_amount = ProductAmount(order=order, product=temp_item.product, amount_of_product=temp_item.amount_of_product)
                        product_amount.save()
                    TempOrder.objects.all().delete()

            elif request.POST.get("Delete"):
                TempOrder.objects.all().delete()

            elif request.POST.get("Delete Item"):
                product = order_creation_data.cleaned_data['to_delete']
                if product != None:
                    TempOrder.objects.get(product=product).delete()

        return HttpResponseRedirect(reverse('ordersys:create'))

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