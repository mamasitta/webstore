from django.urls import path

from store_api import views

urlpatterns = [
    path('', views.test, name='test')
]