from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Generic permission to only allow owners of an object to edit it.
    Supports different ownership models:
    - obj.created_by
    - obj.user

    Can be extended for specific relationship patterns in child classes.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if user is the creator of the object
        if hasattr(obj, "created_by"):
            return obj.created_by == request.user

        # Check if user is the owner of the object
        if hasattr(obj, "user"):
            return obj.user == request.user

        return False


class IsCreatorOrReadOnly(IsOwnerOrReadOnly):
    """
    Alias for IsOwnerOrReadOnly, for clarity when dealing with 'created_by' relationships.
    """

    pass


class IsResourceCreator(permissions.BasePermission):
    """
    Permission to allow only resource creators to manage their resources.
    Works with direct ownership via created_by attribute.

    Can be extended for specific parent-child relationships.
    """

    def has_object_permission(self, request, view, obj):
        # For objects with direct creator relationship
        if hasattr(obj, "created_by"):
            return obj.created_by == request.user

        return False


class IsPublicResourceOrAuthenticated(permissions.BasePermission):
    """
    Allow anonymous access to public resources, but require authentication for private ones.

    This is a base class that should be extended with specific visibility logic.
    By default, it just checks for basic authentication.
    """

    public_visibility_code = "PUBLIC"  # Override in subclasses

    def has_permission(self, request, view):
        # Always allow authenticated users
        if request.user and request.user.is_authenticated:
            return True

        # For anonymous users, only allow safe methods
        if request.method in permissions.SAFE_METHODS:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        # Allow authenticated users full access
        if request.user and request.user.is_authenticated:
            return True

        # Anonymous users only get access to public resources
        # Define visibility check logic in subclasses
        return self.check_public_visibility(obj)

    def check_public_visibility(self, obj):
        """
        Override this method in subclasses to implement specific visibility logic.
        """
        # Default implementation just checks for 'visibility' attribute
        if hasattr(obj, "visibility"):
            return obj.visibility == self.public_visibility_code
        return False


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Allow read-only access to everyone, but write access to staff only.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
