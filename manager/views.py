from django.shortcuts import render
from .models import AccountUser
from .serializers import AccountUserSerializers
from rest_framework import viewsets


class AccountUserViewSet(viewsets.ModelViewSet):
    serializer_class = AccountUserSerializers
    queryset = AccountUser.objects.all()

    def perform_create(self, serializer):
        print("perform_create")
        super().perform_create(serializer)
        # check if role and property are assigned
        # if both are assigned make 2 entries
        # old role = None
        # new role = created role
        # old props
        # new props
        #dfshdfiwsfe






        # try:
        #     account_user = AccountUser.objects.filter(user=serializer.instance.user)
        #     if account_user.count() <= 1:
        #         UserWelcomeEmail(recipients=serializer.instance.user, user=serializer.instance.user).send()
        # except Exception as e:
        #     logger.exception(e)
        # fields = {
        #     'portfolios': serializer.instance.portfolios.values_list('id', flat=True),
        #     'properties': serializer.instance.properties.values_list('id', flat=True),
        # }
        #
        # connection.on_commit(lambda: stream_tasks.create_user.delay(user_id=serializer.instance.user.id, fields=fields))

    def perform_update(self, serializer):
        instance = self.get_object()
        previous_fields = {
            # 'portfolios': list(instance.portfolios.values_list('id', flat=True)),
            'properties': list(instance.properties.values_list('id', flat=True)),
            'role': getattr(instance.role, "pk", None),
        }
        print("perform_update")
        print(previous_fields)
        super().perform_update(serializer)

        # previous_property_ids = set(previous_fields['properties'])
        property_ids = set(list(serializer.instance.properties.values_list('id', flat=True)))
        print(property_ids)
        #
        # fields = {
        #     # 'portfolios': list(set(list(serializer.instance.portfolios.values_list('id', flat=True))).symmetric_difference(
        #     #     previous_fields['portfolios'])),
        #     'properties': list(property_ids.symmetric_difference(previous_fields['properties'])),
        #     'role': (serializer.instance.role.pk,) if serializer.instance.role.pk != previous_fields['role'] else []
        # }

        # connection.on_commit(lambda: stream_tasks.update_user.delay(fields=fields))

        # When an Account User is modified it updates any affected Action Item Approval Step
        # connection.on_commit(lambda: approval_automation_tasks.update_account_user_status_in_approval_steps(
        #     account_user=serializer.instance,
        #     set_role=serializer.instance.role,
        #     unset_role=instance.role,
        #     unset_properties=list(previous_property_ids - property_ids)
        # ))

    # def perform_destroy(self, instance):
    #     fields = {
    #         'portfolios': instance.portfolios.values_list('id', flat=True),
    #         'properties': instance.properties.values_list('id', flat=True),
    #         'role': instance.role.pk,
    #     }
    #     connection.on_commit(lambda: stream_tasks.delete_user.delay(user_id=instance.user.id, fields=fields))
    #     super().perform_destroy(instance)