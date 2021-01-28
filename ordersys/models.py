from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

class Ingredient(models.Model):
    name = models.CharField(max_length=32)
    amount_stored = models.PositiveIntegerField()
    restock_cost = models.DecimalField(max_digits=4, decimal_places=2, default=0)

    def __str__(self):
        return self.name
   
class Product(models.Model):
    name = models.CharField(max_length=32)
    recipe = models.ManyToManyField(Ingredient, through='IngredientAmount')
    cost = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def creation_cost(self):
        cost = 0
        for ingredient_amount in IngredientAmount.objects.filter(product=self):
            cost += ingredient_amount.ingredient.restock_cost\
                    * ingredient_amount.amount
        return cost

    def is_available(self, amount=1):
        for ingredient_amount in IngredientAmount.objects.filter(product=self):
            stock_ingredient = Ingredient.objects.get(name=ingredient_amount.ingredient.name)
            if stock_ingredient.amount_stored\
                - ingredient_amount.amount*amount >= 0:
                continue
            else:
                return False
        return True

    def max_available(self):
        i = 0
        while self.is_available(i):
            i+=1
        return i-1

    def prepare(self, amount=1):
        for ingredient_amount in IngredientAmount.objects.filter(product=self):
            stock_ingredient = Ingredient.objects.get(name=ingredient_amount.ingredient.name)
            stock_ingredient.amount_stored = stock_ingredient.amount_stored - ingredient_amount.amount*amount
            stock_ingredient.save()

    def __str__(self):
        return self.name

class Order(models.Model):
    ordered_items = models.ManyToManyField(Product, through='ProductAmount')
    date_ordered = models.DateTimeField("Ordered", auto_now=True)
    status = models.CharField(max_length=12, default="Pending")
    cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def print_total_cost(self):
        cost = 0
        for product_amount in ProductAmount.objects.filter(order=self):
            cost += product_amount.product.cost * product_amount.amount
        return cost

    def print_ordered_items_products_amounts(self):
        end = ''
        for product_amount in ProductAmount.objects.filter(order=self):
            end += '\n{}: {}, '.format(product_amount.product.name, product_amount.amount)
        return end[:-2]

    def define_shown_id(self):
        if self.id<10:
            return '00{}'.format(self.id)
        elif self.id<100:
            return '0{}'.format(self.id)
        elif self.id<1000:
            return str(self.id)
        else:
            return str(self.id)[-3:]
        
    def __repr__(self):
        return self.id

    def __str__(self):
        return self.define_shown_id()

    
class IngredientAmount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return "Product: {}, Ingredient: {}".format(self.product, self.ingredient)

class ProductAmount(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return "Order: {}, Product: {}".format(self.order, self.product)

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    position = models.CharField(max_length=32)
    employment_date = models.DateField()
    hourly_rate = models.DecimalField(max_digits=4, decimal_places=2)
    minimum_salary = models.DecimalField(max_digits=8, decimal_places=2)

    def get_absolute_url(self):
        return reverse('ordersys:manage_employees')

class TempOrder(models.Model):
    creator = models.ForeignKey(Employee, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount_of_product = models.PositiveIntegerField()

    def print_total_cost(self, request):
        cost = 0
        for item in TempOrder.objects.filter(creator=request.user):
            cost += item.product.cost * amount_of_product
        return cost
