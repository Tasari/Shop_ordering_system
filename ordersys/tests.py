from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.shortcuts import reverse

from ordersys.models import Product, Employee

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
