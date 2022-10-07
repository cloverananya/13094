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

        fields = {
            'properties': serializer.instance.properties.values_list('id', flat=True),
        }
        try:
            serializer.instance.log_role_change(
                source=PermissionLog.ACCOUNT_USER_CREATED,
                type_of_change=PermissionLog.ROLE_CHANGED,
                new_role=serializer.instance.role
            )

            serializer.instance.log_property_change(
                source=PermissionLog.ACCOUNT_USER_CREATED,
                type_of_change=PermissionLog.PROPERTY_CHANGED,
                new_props=list(fields.get('properties')),
                old_props=list()
            )
        except Exception as e:
            # logger.exception(e)
            print(e)
            pass

    def perform_update(self, serializer):
        instance = self.get_object()

        previous_fields = {
            'properties': list(instance.properties.values_list('id', flat=True)),
            'role': getattr(instance.role, "pk", None),
        }

        super().perform_update(serializer)

        previous_property_ids = set(previous_fields['properties'])
        property_ids = set(list(serializer.instance.properties.values_list('id', flat=True)))

        fields = {
            'properties': list(property_ids.symmetric_difference(previous_fields['properties'])),
            'role': (serializer.instance.role.pk,) if serializer.instance.role.pk != previous_fields['role'] else []
        }
        # logging start here
        instance.log_role_change(
            source=PermissionLog.ACCOUNT_USER_UPDATED,
            type_of_change=PermissionLog.ROLE_CHANGED,
            old_role=instance.role,
            new_role=serializer.instance.role
        )

        added_properties = property_ids - previous_property_ids
        removed_properties = previous_property_ids - property_ids

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
        instance.log_role_change(
            source=PermissionLog.ACCOUNT_USER_DELETED,
            type_of_change=PermissionLog.ROLE_CHANGED,
            old_role=instance.role,
        )
        instance.log_property_change(
            source=PermissionLog.ACCOUNT_USER_DELETED,
            type_of_change=PermissionLog.PROPERTY_CHANGED,
            old_props=list(fields.get('properties')),
            new_props=list()
        )
        super().perform_destroy(instance)


class PermissionLogView(viewsets.ModelViewSet):
    serializer_class = PermissionLogSerializers
    queryset = PermissionLog.objects.all()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
