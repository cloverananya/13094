from django.shortcuts import render
from .serializers import AccountSerializer, RoleSerializer, PropertySerializers
from .models import Account, Role, Property
from rest_framework import viewsets


class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()


class RoleViewSet(viewsets.ModelViewSet):
    serializer_class = RoleSerializer
    queryset = Role.objects.all()


class PropertyViewSet(viewsets.ModelViewSet):
    serializer_class = PropertySerializers
    queryset = Property.objects.all()
#     yhjfghghgfh
