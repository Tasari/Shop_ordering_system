from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=32)
    amount_stored = models.PositiveIntegerField()

    def __str__(self):
        return self.name
   
class Product(models.Model):
    name = models.CharField(max_length=32)
    recipe = models.ManyToManyField(Ingredient, through='IngredientAmount')

    def __str__(self):
        return self.name

class Order(models.Model):
    ordered_items = models.ManyToManyField(Product, through='ProductAmount')
    date_ordered = models.DateTimeField("Ordered", auto_now=True)
    status = models.CharField(max_length=12, default="Pending")

    def print_ordered_items_products_amounts(self):
        end = ''
        for item in ProductAmount.objects.filter(order=self):
            end += '\n{}: {}, '.format(item.product.name, item.amount_of_product)
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
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount_of_ingredient = models.PositiveIntegerField()

    def __str__(self):
        return "Product: {}, Ingredient: {}".format(self.product, self.ingredient)

class ProductAmount(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount_of_product = models.PositiveIntegerField()

    def __str__(self):
        return "Order: {}, Product: {}".format(self.order, self.product)

class TempOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount_of_product = models.PositiveIntegerField()



