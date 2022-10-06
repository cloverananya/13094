from rest_framework import serializers
from .models import AccountUser, PermissionLog
from django.contrib.auth.models import User


class AccountUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = AccountUser
        fields = "__all__"

class PermissionLogSerializers(serializers.ModelSerializer):
    class Meta:
        model = PermissionLog
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


