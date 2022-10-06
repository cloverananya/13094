from django.contrib import admin
from django.urls import path ,include
from rest_framework import routers
from core import views as c_views
from manager import views as m_views


router = routers.DefaultRouter()
router.register(r'role', c_views.RoleViewSet)
router.register(r'account', c_views.AccountViewSet)
router.register(r'property', c_views.PropertyViewSet)
router.register(r'accountuser', m_views.AccountUserViewSet)
router.register(r'logs', m_views.PermissionLogView)
router.register(r'users', m_views.UserViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]