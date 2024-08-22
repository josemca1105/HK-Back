from rest_framework import serializers
from .models import Inmuebles
from hk_back.users.serializers import SimpleUserSerializer

class InmueblesSerializer(serializers.ModelSerializer):
    asesor = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Inmuebles
        fields = '__all__'
        read_only_fields = ['asesor']