from django.test import TestCase

# Create your tests here.
from django.urls import resolve

from store_api import views
from store_api.models import User, Product, Order, OrderItem, ProductPicture

""" Models testing"""
class UserTest(TestCase):

    def create_user(self, username='test', email='test', password='test1234567890'):
        return User.objects.create(username=username, email=email, password=password)

    def test_user_creation(self):
        u = self.create_user()
        self.assertTrue(isinstance(u, User))
        self.assertEqual(u.username, 'test')


class ProductTest(TestCase):

    def create_product(self, title='test', description='test case', amount=1, ean='test ean', price=100):
        return Product.objects.create(title=title, description=description, amount=amount, ean=ean, price=price)

    def test_product_creation(self):
        p = self.create_product()
        self.assertTrue(isinstance(p, Product))
        self.assertEqual(p.title, 'test')


class ProductPictureTest(TestCase):

    def create_product(self, title='test', description='test case', amount=1, ean='test ean', price=100):
        return Product.objects.create(title=title, description=description, amount=amount, ean=ean, price=price)

    def create_product_picture(self, product_id=1, image='test/url'):
        return ProductPicture.objects.create(product_id=product_id, image=image)

    def test_product_picture_creation(self):
        p = self.create_product()
        pp = self.create_product_picture()
        self.assertTrue(isinstance(pp, ProductPicture))
        self.assertEqual(pp.product_id, p.id)


class OrderTest(TestCase):

    def create_user(self, username='test', email='test', password='test1234567890'):
        return User.objects.create(username=username, email=email, password=password)

    def create_order(self, user_id='1', address='test address', phone='test phone'):
        return Order.objects.create(user_id=user_id, address=address, phone=phone)

    def test_order_creation(self):
        o = self.create_order()
        u = self.create_user()
        self.assertTrue(isinstance(o, Order))
        self.assertEqual(o.address, 'test address')

class OrderItemTest(TestCase):

    def create_user(self, username='test', email='test', password='test1234567890'):
        return User.objects.create(username=username, email=email, password=password)

    def create_order(self, user_id='1', address='test address', phone='test phone'):
        return Order.objects.create(user_id=user_id, address=address, phone=phone)

    def create_product(self, title='test', description='test case', amount=1, ean='test ean', price=100):
        return Product.objects.create(title=title, description=description, amount=amount, ean=ean, price=price)

    def create_order_item(self, order_id=1, product_id=1, amount=1):
        return OrderItem.objects.create(order_id=order_id, product_id=product_id, amount=1)

    def test_order_creation(self):
        oi = self.create_order_item()
        p = self.create_product()
        o = self.create_order()
        u = self.create_user()
        self.assertTrue(isinstance(oi, OrderItem))
        self.assertEqual(oi.order_id, o.id)






