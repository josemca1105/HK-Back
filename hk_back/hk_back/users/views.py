from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import User
from .serializers import UserSerializer

import jwt, datetime

# Create your views here.

# RegisterView class is used to register a new user
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = Response()
        response.data = {
            'status': status.HTTP_200_OK,
            'message': 'User registered successfully',
            'data': serializer.data
        }
        return response
    
# LoginView class is used to login a user
class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.now(datetime.UTC)
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'status': status.HTTP_200_OK,
            'message': 'User logged in successfully',
            'token': token
        }
        return response
    
# UserView class is used to get the user details
class AuthView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)
    
# LogoutView class is used to logout a user
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'status': status.HTTP_200_OK,
            'message': 'User logged out successfully'
        }
        return response
    
class UsersView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')
        
        serializer = UserSerializer(User.objects.all(), many=True)
        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')
        
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            if 'email' in e.detail:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={
                        'message': 'Email already exists'
                    }
                )
            else:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={
                        'message': f'Invalid data, ${e.detail}'
                    }
                )
        
        serializer.save()
        response = Response()
        response.data = {
            'status': status.HTTP_200_OK,
            'message': 'User created successfully',
            'data': serializer.data
        }
        return response