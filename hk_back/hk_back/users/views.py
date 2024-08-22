from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import User
from .serializers import UserSerializer

import jwt, datetime

from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError

from django.conf import settings

JWT_SECRET = settings.SECRET_KEY

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

        token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'status': status.HTTP_200_OK,
            'message': 'User logged in successfully',
            'token': token
        }
        return response
    
# AuthView class is used to get the user details
class AuthView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
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
    
# UsersListView class is used to get all users
class UsersListView(APIView):
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
    
# UserCreateView class is used to create a new user
class UserCreateView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
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
    
# UserDetailView class is used to retrieve, update or delete a specific user
class UserDetailView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_object(self, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            return None
        
    def get(self, request, id):
        inmueble = self.get_object(id)
        if inmueble is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    'message': 'User no encontrado'
                }
            )
        
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        
        try:
            jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        except (ExpiredSignatureError, InvalidSignatureError):
            raise AuthenticationFailed('Unauthenticated')
        
        serializer = UserSerializer(inmueble)
        response = Response()
        response.data = {
            'status': status.HTTP_200_OK,
            'data': serializer.data
        }
        return response
    
    def patch(self, request, id):
        user = self.get_object(id)
        if user is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    'message': 'User not found'
                }
            )
        
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        
        
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            phone_number = request.data.get('phone', None)
            if phone_number:
                if len(phone_number) < 10:
                    raise ValidationError({'error': 'Phone number must be greater than 10'})
            
            serializer.save()

            response = Response()
            response.data = {
                'status': status.HTTP_200_OK,
                'message': 'User updated successfully',
                'data': serializer.data
            }
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        user = self.get_object(id)
        if user is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    'message': 'User not found'
                }
            )
        
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')
        
        user.delete()
        response = Response()
        response.data = {
            'status': status.HTTP_200_OK,
            'message': f'User {id} deleted successfully'
        }
        return response