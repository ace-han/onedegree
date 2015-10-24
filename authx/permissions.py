from rest_framework import permissions
from rest_framework.permissions import BasePermission, IsAdminUser as DrfIsAdminUser

class IsAdminUser(DrfIsAdminUser):
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)

class IsSuperUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
    
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
    
class IsOwnerOrReadOnly(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        owner = obj.owner if hasattr(obj, 'owner') else obj.user
        if owner:
            return owner.id == request.user.id
        else:
            return False

class SelfOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        owner = obj.owner if hasattr(obj, 'owner') else obj.user
        if owner:
            return owner.id == request.user.id
        else:
            return False