from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import permissions, exceptions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from store_api.models import User
from store_api.serializers import UserSerializer
from store_api.utilits import generate_access_token, generate_refresh_token


def test(request):
    return HttpResponse('Hello Julia')


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
