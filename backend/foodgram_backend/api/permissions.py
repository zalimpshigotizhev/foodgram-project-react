from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Model
from rest_framework.permissions import DjangoModelPermissions  # noqa F401
from rest_framework.permissions import IsAuthenticated  # noqa F401
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.routers import APIRootView


class IsAuthPermission(BasePermission):
    """ Permissin либо просмотры рецептов, либо авторизован"""

    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS
                    or request.user.is_authenticated)


class AuthorStaffOrReadOnly(IsAuthPermission):
    """ Автор или только читать"""

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated
                and (request.user == obj.author or request.user.is_staff))


class AdminOrReadOnly(IsAuthPermission):
    """ Изменение только для авторов """

    def has_object_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated
                and request.user.is_staff)


class OwnerUserOrReadOnly(IsAuthPermission):
    """ Изменения только для админа """

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated
                and request.user == obj.author
                or request.user.is_staff)
