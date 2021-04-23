from django.urls import path

from store_api import views

urlpatterns = [
    path('', views.test, name='test'),
    path('api/login_view', views.login_view, name='login_view'),
    path('api/sign_in', views.sign_in, name='sign_in')
]