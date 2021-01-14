from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.shortcuts import reverse

from ordersys.models import Product

class TestOrderCreationView(TestCase):
    def test_adding_product_to_temp_ord(self):
        user = User.objects.create(username='test')
        user.set_password('12345')
        user.save()

        product = Product(name='Test')
        product.save()
        product = Product.objects.last()
        c = Client()

        response = c.post(reverse('ordersys:login'), {'username':'test', 'password':'12345'}, follow=True)
        response = c.post(reverse('ordersys:create'), {'product':product.id, 'amount':3, 'to_delete':'', 'Add':True})
        response = c.get('/ordersys/orders/create/')
        self.assertContains(response, "Test: 3")

