from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    Read-only for others. Assumes the model instance has an `owner` attribute.
    """
    def has_permission(self, request, view):
        # Allow read-only methods (GET, HEAD, OPTIONS) for anyone.
        if request.method in permissions.SAFE_METHODS:
            return True
        # For write methods (POST, PUT, PATCH, DELETE), user must be authenticated.
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the listing.
        return obj.owner == request.user