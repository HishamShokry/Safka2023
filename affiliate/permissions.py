# myapp/permissions.py

from rest_framework.permissions import BasePermission

class IsVendorOrSuperuserOrImpersonate(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_vendor or request.user.is_superuser or request.user.is_impersonate)

    def has_object_permission(self, request, view, obj):
        # Allow adding new objects
        if request.method == 'POST':
            return True
        # Allow editing or deleting existing objects only if the user is the owner
        elif request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.owner == request.user or request.user.is_superuser or request.user.is_impersonate
        return False

class IsMarketerOrSuperuserOrImpersonate(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_marketer or request.user.is_superuser or request.user.is_impersonate)

    def has_object_permission(self, request, view, obj):
        # Allow adding new objects
        if request.method == 'POST':
            return True
        # Allow editing or deleting existing objects only if the user is the owner
        elif request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.owner == request.user or request.user.is_superuser or request.user.is_impersonate
        return False

class IsAdminOrSuperuserOrImpersonate(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_admin or request.user.is_superuser or request.user.is_impersonate)

    def has_object_permission(self, request, view, obj):
        # Allow adding new objects
        if request.method == 'POST':
            return True
        # Allow editing or deleting existing objects only if the user is the owner
        elif request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.owner == request.user or request.user.is_superuser or request.user.is_impersonate
        return False
