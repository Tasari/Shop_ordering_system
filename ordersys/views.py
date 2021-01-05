from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.http import HttpResponseRedirect
# Create your views here.

from .models import Order, ProductAmountForm, Product, ProductAmount, TempOrderForm

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
    model = ProductAmountForm

    fields = ['product', 'amount']
    def get(self, request):
        context = {'actual_item': ProductAmountForm(), 'order':TempOrderForm()}
        return render(request, self.template_name, context)
    
    def post(self, request):
        product_amount = ProductAmountForm(request.POST)
        if product_amount.is_valid():
            order = Order()
            order.save()
            order = Order.objects.all().last()
            all_products = [Product.objects.get(name=x[1]).id for x in product_amount.fields['product'].iterator(product_amount.fields['product'])]
            all_amounts = product_amount.fields['amount']
            for product, amount in zip(all_products, all_amounts):
                proamo = ProductAmount.objects.create(order=order, product=product, amount_of_product=1)
                proamo.save()

            product_amount.save()
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