from django.db import models
from django.contrib.auth.models import User
from core.models import Account, Role, Property


class AccountUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    properties = models.ManyToManyField(Property)

    def __str__(self):
        return f"{self.user}"

    def log_role_change(self, old_role, new_role):
        pass



class PermissionLog(models.Model):
    Type_of_Change = (
        ("Role", "Role"),
        ("Property", "Property"),
        ("Both", "Both")
    )
    Initiated_BY = (
        ("Update", "Update"),
        ("Create", "Create"),
        ("Delete", "Delete")
    )

    account_user = models.ForeignKey(AccountUser, on_delete=models.CASCADE, related_name='permission_logs')
    type_of_change = models.CharField(choices=Type_of_Change, max_length=300)  ## choice for role, property, both
    initiated_by = models.CharField(choices=Initiated_BY, max_length=300)  ## choice for update, create, delete
    old_role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='+')
    new_role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='+')
    # old_properties = models.M2M('Properties')
    # new_properties = models.M2M('Properties')

    added_properties = models.ManyToManyField(Property, related_name='+')

    deleted_properties = models.ManyToManyField(Property, related_name='+')
