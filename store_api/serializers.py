from rest_framework import serializers

from store_api.models import User, ProductPicture, Product


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


