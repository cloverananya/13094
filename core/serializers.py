from rest_framework import serializers
from .models import Account, Role, Property


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class PropertySerializers(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'
