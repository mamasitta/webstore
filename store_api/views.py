import jwt
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from rest_framework import permissions, exceptions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from store_api.managers.order_manager import check_order_items, save_order_items
from store_api.models import User, Product, Order, OrderItem
from store_api.serializers import UserSerializer, ProductSerializer, OrderItemSerializer, OrderSerializer
from store_api.utilits import generate_access_token, generate_refresh_token
from webstore import settings



@api_view(['POST'])
@permission_classes([permissions.AllowAny,])
@ensure_csrf_cookie
def sign_in(request):
    """ Function to register new user"""
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    if username is None or email is None or password is None:
        content = {'error': "username, email and password required"}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    username_used = User.objects.filter(username=username)
    if username_used:
        content = {'error': "username is used"}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    hashed_password = make_password(password)
    new_user = User(username=username, password=hashed_password, email=email)
    new_user.save()
    content = {'massage': "success"}
    return Response(content, status=status.HTTP_201_CREATED)



@api_view(['POST'])
@permission_classes([permissions.AllowAny,])
@ensure_csrf_cookie
def login_view(request):
    """Function to login user and generate access and refresh tokens
    take from request body: username, password
    return: response
    if success: user object with tokens
    if false: failed massage"""
    User = get_user_model()
    username = request.data.get('username')
    password = request.data.get('password')
    response = Response()
    if username is None or password is None:
        raise exceptions.AuthenticationFailed(
            'username and password required')
    user = User.objects.filter(username=username).first()
    if user is None:
        raise exceptions.AuthenticationFailed('user not found')
    if not user.check_password(password):
        raise exceptions.AuthenticationFailed('wrong password')
    serialized_user = UserSerializer(user).data
    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)
    response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
    response.data = {
        'access_token': access_token,
        'user': serialized_user,
    }
    return response


@api_view(['POST'])
@permission_classes([permissions.AllowAny,])
@csrf_protect
def refresh_token(request):
    """Function to refresh users token need 'X-CSRFTOKEN' param in header (take from cookies in login_view)"""
    User = get_user_model()
    refresh_token = request.COOKIES.get('refreshtoken')
    if refresh_token is None:
        raise exceptions.AuthenticationFailed(
            'Authentication credentials were not provided.')
    try:
        payload = jwt.decode(
            refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed(
            'expired refresh token, please login again.')
    user = User.objects.filter(id=payload.get('user_id')).first()
    if user is None:
        raise exceptions.AuthenticationFailed('User not found')
    if not user.is_active:
        raise exceptions.AuthenticationFailed('user is inactive')
    access_token = generate_access_token(user)
    return Response({'access_token': access_token})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_protect
def get_all_products(request):
    """Function return all products"""
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_protect
def get_order(request):
    """Function return or users order or if user admin return requested orders from param"""
    username = request.user
    user = User.objects.filter(username=username).first()
    # if user admin, return orders according params
    if user.is_superuser:
        if 'category' in request.GET:
            category = request.GET['category']
            if category == 'completed':
                order = Order.objects.filter(complete=True)
            elif category == 'uncompleted':
                order = Order.objects.filter(complete=False)
            elif category == 'user':
                if 'user_id' in request.GET:
                    user_id = request.GET['user_id']
                    order = Order.objects.filter(user_id=user_id)
                else:
                    content = {'error': "user id is required"}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            order = Order.objects.all()
    # if user is not admin, return users orders
    else:
        order = Order.objects.filter(user_id=user.id)
    serializer = OrderSerializer(order, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_protect
def post_order(request):
    """Function save order from user, return order data"""
    username = request.user
    user = User.objects.filter(username=username).first()
    address = request.data.get('address')
    phone = request.data.get('phone')
    items = request.data.get('items')
    if address is None or phone is None or items is None or len(items) == 0:
        content = {"error": "address, phone, and ordered items are required"}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    for item in items:
        check_product = check_order_items(item)
        if not check_product:
            content = {"error": "product is not valid or do not have enough amount of items"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
    # register new order
    new_order = Order(user_id=user.id, address=address, phone=phone)
    new_order.save()
    order = Order.objects.filter(user_id=user.id).order_by('-id')[0]
    # should be added more checks for data
    for item in items:
        # change amount of product in db and register new items for order
        save_item = save_order_items(item=item, order_id=order.id)
        if not save_item:
            content = {"error": "order was not complete"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
    serializer = OrderSerializer(order)
    return Response(serializer.data)






