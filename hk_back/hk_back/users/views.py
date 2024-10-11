from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import User
from .serializers import UserSerializer, ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from django.template.loader import render_to_string

import jwt, datetime

from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError

from django.conf import settings

JWT_SECRET = settings.SECRET_KEY

# Create your views here.

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
        user = self.get_object(id)
        if user is None:
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
        
        serializer = UserSerializer(user)
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
        
        try:
            jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        except (ExpiredSignatureError, InvalidSignatureError):
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
    
# Recuperar contraseña
class RequestPasswordResetEmail(APIView):
    def post(self, request):
        serializer = ResetPasswordEmailRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            # current_site = get_current_site(request=request).domain
            # relative_link = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            absurl = f'http://localhost:4200/reestablecer-clave/{uidb64}/{token}'
            #email_body = f'Hola {user.name},\nUsa este link para restablecer tu contraseña {absurl}'
            user_name = user.f_name.capitalize()

            context = {
                'user': user,
                'reset_link': absurl,
                'user_name': user_name
            }
            html_message = render_to_string("reset-password.html", context)
            data = {
                'email_body': html_message,
                'to_email': [user.email],
                'email_subject': 'Restablecer contraseña'
            }
            try:
                Util.send_email(data)
                return Response(
                    {'success': 'Se ha enviado el link para restablecer tu contraseña'},
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                print(f'Error sending email: {e}')
                return Response(
                    {'error': 'Error al enviar el correo electrónico'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(
            {'error': 'Email not found'},
            status=status.HTTP_404_NOT_FOUND
        )

# PasswordTokenCheck class is used to check if the token is valid
class PasswordTokenCheck(APIView):
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({
                'success': True,
                'message': 'Credentials valid',
                'uidb64': uidb64,
                'token': token
            }, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError:
            return Response({'error': 'Token is not valid, please request a new one'},
                            status=status.HTTP_401_UNAUTHORIZED)

# SetNewPassword class is used to set a new password
class SetNewPassword(APIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            print('Serializer is valid.')
            return Response(
                {'success': True, 'message': 'Password reset success'
                }, status=status.HTTP_200_OK)
        else:
            print('Serializer is invalid.')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
