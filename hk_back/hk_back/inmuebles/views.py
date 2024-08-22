from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from .models import Inmuebles
from hk_back.users.models import User
from .serializers import InmueblesSerializer

import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError

from django.conf import settings

JWT_SECRET = settings.SECRET_KEY

# Create your views here.

# InmueblesPersonalView class is used to get inmuebles of the logged in user
class InmueblesPersonalView(APIView):
    def get(self, request):
        user = User.objects.filter(id=payload['id']).first()
        if user is None:
            raise AuthenticationFailed('User not found')
        
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        except (ExpiredSignatureError, InvalidSignatureError):
            raise AuthenticationFailed('Unauthenticated')
        
        serializer = InmueblesSerializer(Inmuebles.objects.filter(asesor=user), many=True)
        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )

# InmueblesAllView class is used to get all inmuebles
class InmueblesAllView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        
        try:
            jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        except (ExpiredSignatureError, InvalidSignatureError):
            raise AuthenticationFailed('Unauthenticated')
        
        serializer = InmueblesSerializer(Inmuebles.objects.all(), many=True)
        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )

# InmueblesCreateView class is used to create a new inmueble
class InmueblesCreateView(APIView):
    def post(self, request):
        user = User.objects.filter(id=payload['id']).first()
        if user is None:
            raise AuthenticationFailed('User not found')
        
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        except (ExpiredSignatureError, InvalidSignatureError):
            raise AuthenticationFailed('Unauthenticated')
        
        data = request.data.copy()
        data['asesor'] = user.id

        serializer = InmueblesSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(asesor=user)

        response = Response()
        response.data = {
            'status': status.HTTP_200_OK,
            'message': 'Inmueble creado exitosamente',
            'data': serializer.data
        }
        return response
    
# InmuebleDetailView is used to retrieve, update or delete a specific inmueble
class InmuebleDetailView(APIView):
    def get_object(self, id):
        try:
            return Inmuebles.objects.get(pk=id)
        except Inmuebles.DoesNotExist:
            return None
        
    def get(self, request, id):
        inmueble = self.get_object(id)
        if inmueble is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    'message': 'Inmueble no encontrado'
                }
            )
        
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        
        try:
            jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        except (ExpiredSignatureError, InvalidSignatureError):
            raise AuthenticationFailed('Unauthenticated')
        
        serializer = InmueblesSerializer(inmueble)
        response = Response()
        response.data = {
            'status': status.HTTP_200_OK,
            'data': serializer.data
        }
        return response