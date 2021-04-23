import json

from rest_framework import serializers

from store_api.models import User, ProductPicture, Product, OrderItem, Order


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ProductImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPicture
        fields = ['image']


class ProductSerializer(serializers.ModelSerializer):
    product_img = ProductImgSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'amount', 'ean', 'price', 'product_img']


class OrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title')
    product_description = serializers.CharField(source='product.description')
    product_ean = serializers.CharField(source='product.ean')
    product_price = serializers.CharField(source='product.price')
    class Meta:
        model = OrderItem
        fields = ['product_description', 'product_ean', 'product_title', 'product_price', 'amount']


class OrderSerializer(serializers.ModelSerializer):
    order_item = OrderItemSerializer(many=True)
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')

    class Meta:
        model = Order
        fields = ['username', 'email', 'date_ordered', 'date_complete', 'address', 'phone', 'order_item']


# class OrderSerial(serializers.ModelSerializer):
#
#     class Meta:
#         model= OrderItem
#         fields = ['__all__']
#
#
#
# class OrderItemSerializer():
#
#     def serialized_data(self, item):
#         data = {
#             'product': OrderItemSerializer.get_product(item['id']),
#             'amount': item['amount']
#         }
#         return data
#
#     def get_product(self, product_id):
#         product = Product.objects.filter(id=product_id).first()
#         return product
#
#
# class OrderSerializer():
#     def __init__(self, order):
#         self.items = self.get_items(order_id=order['id'])
#
#     def get_items(self, order_id):
#         items = OrderItem.objects.filter(order_id=order_id).all()
#         return items
#
#     def serialized_data(self, order):
#         order = {
#             'id': order['id'],
#             'date_ordered': order['date_ordered'].strftime('%B %d, %Y'),
#             'date_complete': order['date_complete'],
#             'address': order['address'],
#             'phone': order['phone'],
#             'complete': order['complete'],
#             'order_items': self.items,
#             # 'total_payment':
#
#         }
#     def total_price(self, items):
#         total = 0
#         for item in items:
#             print(item)



