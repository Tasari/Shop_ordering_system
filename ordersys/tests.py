from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.shortcuts import reverse

from ordersys.models import *
class TestOrderCreationView(TestCase):
    def setUp(self):
        user = User.objects.create(username='test')
        user.set_password('12345')
        user.save()
        employee = Employee.objects.create(
            user=User.objects.last(), 
            first_name='test',
            last_name='test',
            position='test',
            employment_date = '2021-01-25',
            hourly_rate=1.50,
            minimum_salary = 15.50
        )
        product = Product(name='Test')
        product2 = Product(name='Test2')
        product.save()
        product2.save()
        self.c = Client()
        response = self.c.post(reverse('ordersys:login'), {'username':'test', 'password':'12345'}, follow=True)
    
    def test_adding_products_to_temp_ord(self):
        product = Product.objects.last()
        amount = 3
        response = self.c.post(reverse('ordersys:create'), {'product':product.id, 'amount':amount, 'Add':True})
        response = self.c.get(reverse('ordersys:create'))
        self.assertContains(response, "{}: {}".format(product.name, amount))

    def test_adding_same_product_twice(self):
        product = Product.objects.last()
        amount = 3
        amount2 = 2
        response = self.c.post(reverse('ordersys:create'), {'product':product.id, 'amount':amount, 'Add':True})
        response = self.c.post(reverse('ordersys:create'), {'product':product.id, 'amount':amount2, 'Add':True})
        response = self.c.get(reverse('ordersys:create'))
        self.assertContains(response, "{}: {}".format(product.name, amount+amount2))

    def test_adding_two_products(self):
        product = Product.objects.get(id=1)
        product2 = Product.objects.get(id=2)
        amount = 3
        response = self.c.post(reverse('ordersys:create'), {'product':product.id, 'amount':amount, 'Add':True})
        response = self.c.post(reverse('ordersys:create'), {'product':product2.id, 'amount':amount, 'Add':True})
        response = self.c.get(reverse('ordersys:create'))
        self.assertContains(response, "{}: {}".format(product.name, amount))
        self.assertContains(response, "{}: {}".format(product2.name, amount))

    def test_adding_negative_product_amount(self):
        product = Product.objects.last()
        amount = -3
        response = self.c.post(reverse('ordersys:create'), {'product':product.id, 'amount':amount, 'Add':True})
        response = self.c.get(reverse('ordersys:create'))
        self.assertNotContains(response, "{}: {}".format(product.name, amount))

    def test_subtracting_amount_from_product(self):
        product = Product.objects.last()
        amount = 3
        amount2 = -2
        response = self.c.post(reverse('ordersys:create'), {'product':product.id, 'amount':amount, 'Add':True})
        response = self.c.post(reverse('ordersys:create'), {'product':product.id, 'amount':amount2, 'Add':True})
        response = self.c.get(reverse('ordersys:create'))
        self.assertContains(response, "{}: {}".format(product.name, amount+amount2))

    def test_subtracting_higher_amount_from_product(self):
        product = Product.objects.last()
        amount = 3
        amount2 = -5
        response = self.c.post(reverse('ordersys:create'), {'product':product.id, 'amount':amount, 'Add':True})
        response = self.c.post(reverse('ordersys:create'), {'product':product.id, 'amount':amount2, 'Add':True})
        response = self.c.get(reverse('ordersys:create'))
        self.assertContains(response, "{}: {}".format(product.name, amount))
    
    def test_deleting_from_order(self):
        product = Product.objects.last()
        amount = 3
        response = self.c.post(reverse('ordersys:create'), {'product':product.id, 'amount':amount, 'Add':True})
        response = self.c.post(reverse('ordersys:create'), {'to_delete':product.id, 'Delete Item':True})
        response = self.c.get(reverse('ordersys:create'))
        self.assertNotContains(response, "{}: {}".format(product.name, amount))

    def test_deleting_order(self):
        product = Product.objects.get(id=1)
        product2 = Product.objects.get(id=2)
        amount = 3
        response = self.c.post(reverse('ordersys:create'), {'product':product.id, 'amount':amount, 'Add':True})
        response = self.c.post(reverse('ordersys:create'), {'product':product2.id, 'amount':amount, 'Add':True})
        response = self.c.post(reverse('ordersys:create'), {'Delete':True})
        response = self.c.get(reverse('ordersys:create'))
        self.assertNotContains(response, "{}: {}".format(product.name, amount))
        self.assertNotContains(response, "{}: {}".format(product2.name, amount))
    
    def test_finishing_order(self):
        product = Product.objects.get(id=1)
        product2 = Product.objects.get(id=2)
        amount = 3
        response = self.c.post(reverse('ordersys:create'), {'product':product.id, 'amount':amount, 'Add':True})
        response = self.c.post(reverse('ordersys:create'), {'product':product2.id, 'amount':amount, 'Add':True})
        response = self.c.post(reverse('ordersys:create'), {'Finish':True})
        response = self.c.get(reverse('ordersys:index'))
        self.assertContains(response, "{}: {}".format(product.name, amount))
        self.assertContains(response, "{}: {}".format(product2.name, amount))

class TestProductObject(TestCase):
    def setUp(self):
        product = Product.objects.create(name="Test")
        product.save()
        ingredient1 = Ingredient.objects.create(name="TestIngre1", amount_stored=1, restock_cost=0.50)
        ingredient1.save()
        ingredient2 = Ingredient.objects.create(name="TestIngre2", amount_stored=1, restock_cost=1.50)
        ingredient2.save()
        ia1 = IngredientAmount.objects.create(product=product, ingredient=ingredient1, amount=1)
        ia1.save()
        ia2 = IngredientAmount.objects.create(product=product, ingredient=ingredient2, amount=1)
        ia2.save()
    
    def test_creation_cost(self):
        product = Product.objects.get(name="Test")
        assert(product.creation_cost()==2)
    
    def test_product_available(self):
        product = Product.objects.get(name="Test")
        assert(product.is_available(1) == True)
        assert(product.is_available(2) == False)

class TestOrderObject(TestCase):
    def setUp(self):
        order = Order.objects.create()
        order.save()
        product = Product.objects.create(name="Test", cost=5.00)
        product.save()
        ingredient1 = Ingredient.objects.create(name="TestIngre1", amount_stored=1, restock_cost=0.50)
        ingredient1.save()
        ingredient2 = Ingredient.objects.create(name="TestIngre2", amount_stored=1, restock_cost=1.50)
        ingredient2.save()
        ia1 = IngredientAmount.objects.create(product=product, ingredient=ingredient1, amount=1)
        ia1.save()
        ia2 = IngredientAmount.objects.create(product=product, ingredient=ingredient2, amount=1)
        ia2.save()
        pa1 = ProductAmount(order=order, product=product, amount=2)
        pa1.save()  

    def test_total_cost(self):
        order=Order.objects.last()
        assert(order.print_total_cost() == 10)

    def test_products_amount_print(self):
        order = Order.objects.last()
        assert(order.print_ordered_items_products_amounts() == "\nTest: 2")