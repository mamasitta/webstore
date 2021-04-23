from django.urls import path

from store_api import views

urlpatterns = [
    # registration, authentication
    path('api/login_view', views.login_view, name='login_view'),
    path('api/refresh_token', views.refresh_token, name='refresh_token'),
    path('api/sign_in', views.sign_in, name='sign_in'),
    # get products and orders
    path('api/get_all_products', views.get_all_products, name='get_all_products'),
    path('api/get_order', views.get_order, name='get_order'),
    # post order
    path('api/post_order', views.post_order, name='post_order'),
]