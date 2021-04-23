from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField()
    password = models.CharField(max_length=255)


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    amount = models.IntegerField()
    ean = models.CharField(max_length=13)
    price = models.IntegerField()


# class Order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
#     date_ordered = models.DateTimeField()
#     date_complete = models.DateTimeField(null=True)
#     address = models.TextField()
#     phone = models.CharField(max_length=20)
#     complete = models.BooleanField(default=False)
#
#
# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_item')
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_item')
#     amount = models.IntegerField()


class ProductPicture(models.Model):
    """class for product img for frontend views """
    # in production media root should be set to server like S3
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_img')
    image = models.ImageField(upload_to='product_img')

