from typing import Union

from django.db import models
from django.contrib.auth.models import User
from core.models import Account, Role, Property
from django.utils.translation import gettext_lazy as _


class AccountUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)
    properties = models.ManyToManyField(Property, blank=True)

    def __str__(self):
        return f"{self.user}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None, skip_role=False):
        super(AccountUser, self).save(force_insert, force_update, using, update_fields)

        # old_props = self.properties.all()
        # print(old_props)
        # globals(old_props)

        save_again = False

        if self.role is not None and skip_role is False:
            save_again = True

        if save_again:
            super(AccountUser, self).save()

    def log_role_change(
            self,
            source: str,
            type_of_change: str,
            old_role: Role = None,
            new_role: Role = None,
    ) -> None:
        if old_role != new_role:

            PermissionLog.objects.create(
                account_user=self,
                type=type_of_change,
                source=source,
                old_role=old_role,
                new_role=new_role
            )

    def log_property_change(
            self,
            source: str,
            type_of_change: str,
            old_props: Union[list, set] = None,
            new_props: Union[list, set] = None
    ) -> None:
        if old_props != new_props:
            log = PermissionLog.objects.create(
                account_user=self,
                type=type_of_change,
                source=source,
            )

            log.added_properties.set(new_props)
            log.deleted_properties.set(old_props)


class PermissionLog(models.Model):
    """
    This is the representation of an Account User's permission logs within the platform.
    Attributes:
       account_user (ForeignKey): AccountUser Model
       type (Char choice): Type of change
       source (Char choice): Source of change
       old_role (ForeignKey): AccountUserRole Model
       new_role (ForeignKey): AccountUserRole Model
       added_properties (ManyToManyField): Property Model
       deleted_properties (ManyToManyField): Property Model
       email (EmailField): User Email Address

    """

    ROLE_CHANGED = 'ROLE'
    PROPERTY_CHANGED = 'PROPERTY'

    ACCOUNT_USER_CREATED = 'CREATED'
    ACCOUNT_USER_UPDATED = 'UPDATED'
    ACCOUNT_USER_DELETED = 'DELETED'

    TYPE_OF_CHANGE = [
        (ROLE_CHANGED, _('Role Changed')),
        (PROPERTY_CHANGED, _('Property changed')),
    ]

    SOURCE_OF_CHANGE = (
        (ACCOUNT_USER_CREATED, "User Created"),
        (ACCOUNT_USER_UPDATED, "User Updated"),
        (ACCOUNT_USER_DELETED, "User Deleted")
    )

    account_user = models.ForeignKey(AccountUser, on_delete=models.SET_NULL, null=True, related_name='permission_logs')
    type = models.CharField(choices=TYPE_OF_CHANGE, max_length=20)
    source = models.CharField(choices=SOURCE_OF_CHANGE, max_length=20)
    old_role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    new_role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    added_properties = models.ManyToManyField(Property, related_name='+', blank=True)
    deleted_properties = models.ManyToManyField(Property, related_name='+', blank=True)

    email = models.EmailField(max_length=250)

    def save(self, *args, **kwargs):
        if not self.id:
            self.email = self.account_user.user.username
        super(PermissionLog, self).save(*args, **kwargs)
