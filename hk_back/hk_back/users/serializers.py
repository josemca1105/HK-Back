from rest_framework import serializers
from .models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode
from rest_framework.exceptions import AuthenticationFailed

import random
import string

from .utils import Util

def generate_password():
    characters = string.ascii_letters + string.digits + "*"
    while True:
        password = ''.join(random.choice(characters) for i in range(8))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and any(c.isdigit() for c in password)
                and any(c in "*!" for c in password)):
            break
    return password

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['f_name']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'f_name', 'l_name', 'email', 'password', 'phone', 'role', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }

    def create(self, validated_data):
        # Generar una contraseña si no se proporciona
        password = generate_password()  # Generar la contraseña
        validated_data['password'] = password  # Asignar la contraseña generada
        instance = self.Meta.model(**validated_data)

        # Establecer la contraseña generada
        instance.set_password(password)
        instance.save()

        # Enviar la contraseña al correo del usuario
        email_body = f'Hola {instance.f_name},\nTu cuenta ha sido creada y tu contraseña es: {password}'
        data = {
            'email_body': email_body,
            'to_email': [instance.email],
            'email_subject': 'Tu nueva cuenta ha sido creada'
        }
        Util.send_email(data)

        return instance
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        if password is not None:
            instance.set_password(password)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
    
class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)
    
    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email', '')
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email not found')
        return attrs

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'uidb64', 'token']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError('Token is not valid, please request a new one')

            user.set_password(password)
            user.save()

            return attrs
        except DjangoUnicodeDecodeError as identifier:
            raise serializers.ValidationError('Token is not valid, please request a new one')