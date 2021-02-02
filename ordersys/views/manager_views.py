from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

from ..forms import *
from ..models import *

class ManagerMenuView(LoginRequiredMixin, generic.CreateView):
    login_url = '/ordersys/login/'
    template_name = 'ordersys/manager/manager_tab.html'
    
    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        if request.POST.get("Report"):
            return HttpResponseRedirect(reverse('ordersys:manage_reports'))
        if request.POST.get("Employees"):
            return HttpResponseRedirect(reverse('ordersys:manage_employees'))
        if request.POST.get("Orders"):
            return HttpResponseRedirect(reverse('ordersys:manage_orders')) 
        if request.POST.get("Stock"):
            return HttpResponseRedirect(reverse('ordersys:manage_stock'))

class ManageOrdersView(LoginRequiredMixin, generic.ListView):
    login_url = '/ordersys/login/' 
    template_name = 'ordersys/manager/manage_orders.html'
    model = Order
    context_object_name = 'orders_list'

    def get_queryset(self):
        return Order.objects.order_by('-date_ordered')

class ManageEmployeesView(LoginRequiredMixin, generic.ListView):
    login_url = '/ordersys/login/' 
    template_name = 'ordersys/manager/manage_employees.html'
    model = Employee
    context_object_name = 'employees_list'

    def get_queryset(self):
        return Employee.objects.order_by('id')

class EmployeeDetailsView(generic.DetailView):
    model = Employee
    template_name = 'ordersys/manager/employee_details.html'

class EmployeeUpdateView(generic.edit.UpdateView):
    model = Employee
    template_name='ordersys/manager/edit_employee.html'
    fields = ['first_name', 'last_name', 'position', 'hourly_rate']

    def post(self, request, pk):
        new_employee_data = EditEmployeeForm(request.POST)
        employee = get_object_or_404(Employee, pk=pk)
        if new_employee_data.is_valid():
            first_name = new_employee_data.cleaned_data["first_name"]
            last_name = new_employee_data.cleaned_data["last_name"]
            position = new_employee_data.cleaned_data["position"]
            hourly_rate = new_employee_data.cleaned_data["hourly_rate"]
            if request.POST.get("Update"):
                employee.first_name = first_name
                employee.last_name = last_name
                employee.position = position
                employee.hourly_rate = hourly_rate
                employee.minimum_salary = hourly_rate*160
                employee.save()
            elif request.POST.get("Fire"):
                employee.delete()
            elif request.POST.get("Promote"):
                employee.promote()
            elif request.POST.get("Demote"):
                employee.demote()
        return HttpResponseRedirect(reverse("ordersys:manage_employees"))
                

class OrderDetailsView(generic.DetailView):
    model = Order
    template_name = 'ordersys/manager/order_details.html'

class OrderUpdateView(generic.edit.UpdateView):
    model = Order
    template_name='ordersys/manager/edit_order.html'
    fields = ['status']
    
    def post(self, request, pk):
        order_data = EditOrderForm(request.POST)
        order = get_object_or_404(Order, pk=pk)
        if order_data.is_valid():    
            status = order_data.cleaned_data['status']
            order.status = status
            order.save()
        return HttpResponseRedirect(reverse('ordersys:order_details', args=[pk]))

class ManageStockView(LoginRequiredMixin, generic.ListView):
    login_url = '/ordersys/login/' 
    template_name = 'ordersys/manager/manage_stock.html'
    model = Ingredient
    context_object_name = 'ingredients_list'

    def get_queryset(self):
        return Ingredient.objects.order_by('name')

class IngredientDetailsView(generic.DetailView):
    model = Ingredient
    template_name = 'ordersys/manager/ingredient_details.html'

class IngredientRestockView(generic.DetailView):
    model = Ingredient
    template_name='ordersys/manager/restock_ingredient.html'
    def get(self, request, pk):
        context = {
            'form': RestockIngredientForm(),
            'ingredient': get_object_or_404(Ingredient, pk=pk),
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        new_ingredient_data = RestockIngredientForm(request.POST)
        ingredient = get_object_or_404(Ingredient, pk=pk)
        if new_ingredient_data.is_valid():
            amount_to_restock = new_ingredient_data.cleaned_data["amount_to_restock"]
            if request.POST.get("Restock"):
                ingredient.amount_stored = ingredient.amount_stored + amount_to_restock
                ingredient.save()
        return HttpResponseRedirect(reverse("ordersys:manage_stock"))

class IngredientUpdateView(generic.edit.UpdateView):
    model = Ingredient
    template_name='ordersys/manager/edit_ingredient.html'
    fields = ['name', 'amount_stored']

    def post(self, request, pk):
        new_ingredient_data = EditIngredientForm(request.POST)
        ingredient = get_object_or_404(Ingredient, pk=pk)
        if new_ingredient_data.is_valid():
            name = new_ingredient_data.cleaned_data["name"]
            amount_stored = new_ingredient_data.cleaned_data["amount_stored"]
            if request.POST.get("Update"):
                ingredient.name = name
                ingredient.amount_stored = amount_stored
                ingredient.save()
        return HttpResponseRedirect(reverse("ordersys:manage_stock"))

class TodayView(LoginRequiredMixin, generic.dates.TodayArchiveView):
    queryset = Order.objects.all()
    date_field = 'date_ordered'
    allow_future = True
    template_name = 'ordersys/manager/archive_day.html'