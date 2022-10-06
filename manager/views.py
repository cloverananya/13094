from core.models import Role
from .models import AccountUser, PermissionLog
from .serializers import AccountUserSerializers, PermissionLogSerializers, UserSerializer
from rest_framework import viewsets
from django.contrib.auth.models import User


class AccountUserViewSet(viewsets.ModelViewSet):
    serializer_class = AccountUserSerializers
    queryset = AccountUser.objects.all()

    def perform_create(self, serializer):
        super().perform_create(serializer)

        acu = serializer.instance
        if serializer.instance.role:
            acu.log_role_change(
                source=PermissionLog.ACCOUNT_USER_CREATED,
                type_of_change=PermissionLog.ROLE_CHANGED,
                new_role=serializer.instance.role
            )

        new_props = serializer.instance.properties.all()
        if new_props:
            acu.log_property_change(
                source=PermissionLog.ACCOUNT_USER_CREATED,
                type_of_change=PermissionLog.PROPERTY_CHANGED,
                new_props=new_props
            )

    def perform_update(self, serializer):
        instance = self.get_object()
        previous_fields = {
            'properties': list(instance.properties.values_list('id', flat=True)),
            'role': getattr(instance.role, "pk", None),
        }
        super().perform_update(serializer)

        if previous_fields.get("role"):
            old_role = Role.objects.get(id=previous_fields.get("role"))
        else:
            old_role = None

        if serializer.instance.role:
            new_role = serializer.instance.role
        else:
            new_role = None

        role_changed = new_role != old_role
        if role_changed:
            instance.log_role_change(
                source=PermissionLog.ACCOUNT_USER_UPDATED,
                type_of_change=PermissionLog.ROLE_CHANGED,
                old_role=old_role,
                new_role=new_role
            )

        previous_property_ids = set(previous_fields['properties'])
        new_property_ids = set(list(serializer.instance.properties.values_list('id', flat=True)))
        added_properties = new_property_ids - previous_property_ids
        removed_properties = previous_property_ids - new_property_ids

        if added_properties or removed_properties:
            instance.log_property_change(
                source=PermissionLog.ACCOUNT_USER_UPDATED,
                type_of_change=PermissionLog.PROPERTY_CHANGED,
                new_props=added_properties,
                old_props=removed_properties
            )

    def perform_destroy(self, instance):
        fields = {
            'properties': instance.properties.values_list('id', flat=True),
            'role': getattr(instance.role, "pk", None)
        }

        if fields.get('role'):
            role = Role.objects.get(id=fields.get('role'))
            instance.log_role_change(
                source=PermissionLog.ACCOUNT_USER_DELETED,
                type_of_change=PermissionLog.ROLE_CHANGED,
                old_role=role
            )
        if fields.get('properties'):
            props = fields.get('properties')
            instance.log_property_change(
                source=PermissionLog.ACCOUNT_USER_DELETED,
                type_of_change=PermissionLog.PROPERTY_CHANGED,
                old_props=props
            )
        super().perform_destroy(instance)


class PermissionLogView(viewsets.ModelViewSet):
    serializer_class = PermissionLogSerializers
    queryset = PermissionLog.objects.all()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
