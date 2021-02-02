from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

from ..forms import *
from ..models import *

class OrdersView(LoginRequiredMixin, generic.ListView):
    login_url = '/ordersys/login/'
    model=Order
    template_name = 'ordersys/order/orders.html'
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
    template_name = 'ordersys/order/customers.html'
    context_object_name = 'orders_list'
    orderint = ['id']

    def get_queryset(self):
        return Order.objects.exclude(status='Done').all()

class CreateOrderView(LoginRequiredMixin, generic.CreateView):
    login_url = '/ordersys/login/'
    template_name = 'ordersys/order/create_order.html'
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
                self.delete_order()
            elif request.POST.get("Delete Item"):
                self.delete_from_order(deletion)
        return HttpResponseRedirect(reverse('ordersys:create'))

    def get_employee_id(self):
        return Employee.objects.get(user_id=self.request.user.id).id

    def add_to_order(self, product, amount):
        maximum = product.max_available()
        try:
            product_on_temp = TempOrder.objects.get(product=product)
            if product_on_temp:
                if product_on_temp.amount_of_product + amount > 0:
                    if amount > maximum:
                        amount = maximum
                    product_on_temp.amount_of_product += amount
                    product_on_temp.product.prepare(amount)
                    product_on_temp.save()
        except:    
            if product != None and amount!= None and amount > 0 and maximum > 0:
                if amount > maximum:
                    amount = maximum
                product.prepare(amount)
                employee_id = Employee.objects.get()
                temp_order = TempOrder(
                    creator_id = self.get_employee_id(),
                    product=product, 
                    amount_of_product=amount
                    )
                temp_order.save()

    def finish_order(self):
        if TempOrder.objects.all():
            order = Order()
            order.save()
            order = Order.objects.last()
            for temp_item in TempOrder.objects.filter(creator_id=self.get_employee_id()):
                product_amount = ProductAmount(
                    order=order, 
                    product=temp_item.product, 
                    amount=temp_item.amount_of_product
                    )
                product_amount.save()
            TempOrder.objects.all().delete()
    
    def delete_from_order(self, to_delete):
        if to_delete != None:
            to_delete_product = TempOrder.objects.get(product=to_delete, creator_id=self.get_employee_id())
            to_delete_product.product.prepare(-to_delete_product.amount_of_product)
            to_delete_product.delete()
    def delete_order(self):
        for to_delete in TempOrder.objects.filter(creator_id=self.get_employee_id()):
            self.delete_from_order(to_delete.product)

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