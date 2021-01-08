from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.http import HttpResponseRedirect
# Create your views here.

from .models import Order, Product, ProductAmount, TempOrder
from .forms import OrderCreationForm

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

class CreateOrderView(generic.CreateView):
    template_name = 'ordersys/create_order.html'
    model = OrderCreationForm

    fields = ['product', 'amount']
    def get(self, request):
        context = {'item_amount': OrderCreationForm(), 'temp_ord': TempOrder.objects.all()}
        return render(request, self.template_name, context)
    
    def post(self, request):
        product_amount = OrderCreationForm(request.POST)
        if product_amount.is_valid():
            if request.POST.get("Add"):
                product = product_amount.cleaned_data['product']
                amount = product_amount.cleaned_data['amount']
                try:
                    product_on_temp = TempOrder.objects.get(product=product)
                    if product_on_temp:
                        product_on_temp.amount_of_product += amount
                        product_on_temp.save()
                except:    
                    if product != None and amount!=None:
                        order = TempOrder(product=product, amount_of_product=amount)
                        order.save()

            elif request.POST.get("Finish"):
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
                product = product_amount.cleaned_data['to_delete']
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