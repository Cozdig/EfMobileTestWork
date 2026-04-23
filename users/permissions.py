from rest_framework.permissions import BasePermission
from .models import RolePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'manager'

class IsAdminOrManager(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ['admin', 'manager']

class IsAdminOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        return obj.user == request.user

class CanViewProducts(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

class CanEditProducts(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method == 'GET':
            return True
        return request.user.role in ['admin', 'manager']

class CanDeleteProducts(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method == 'DELETE':
            return request.user.role == 'admin'
        return True


class HasPermission(BasePermission):

    def __init__(self, permission_codename):
        self.permission_codename = permission_codename

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        return RolePermission.objects.filter(
            role=request.user.role,
            permission__codename=self.permission_codename
        ).exists()


def can_view_product():
    return HasPermission('can_view_product')


def can_create_product():
    return HasPermission('can_create_product')


def can_edit_product():
    return HasPermission('can_edit_product')


def can_delete_product():
    return HasPermission('can_delete_product')


def can_view_user():
    return HasPermission('can_view_user')


def can_edit_user():
    return HasPermission('can_edit_user')


def can_delete_user():
    return HasPermission('can_delete_user')


def can_manage_roles():
    return HasPermission('can_manage_roles')