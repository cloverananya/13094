from django.contrib import admin
from .models import AccountUser,PermissionLog


admin.site.register(AccountUser)
admin.site.register(PermissionLog)
