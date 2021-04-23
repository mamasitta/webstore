from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from store_api.models import User, Product, ProductPicture

admin.site.register(User, UserAdmin)
admin.site.register(Product)
admin.site.register(ProductPicture)
