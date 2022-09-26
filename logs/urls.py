from django.contrib import admin
from django.urls import path ,include
from rest_framework import routers
from core.views import RoleViewSet, AccountViewSet, PropertyViewSet
from manager.views import AccountUserViewSet

router = routers.DefaultRouter()
router.register(r'role', RoleViewSet)
router.register(r'account', AccountViewSet)
router.register(r'property', PropertyViewSet)
router.register(r'accountuser',AccountUserViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]