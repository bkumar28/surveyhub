from rest_framework import permissions


class IsSurveyOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of a survey to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the survey.
        return obj.created_by == request.user


class IsAuthenticatedOrReadOnlyForPublicSurveys(permissions.BasePermission):
    """
    Allow anonymous users to respond to public surveys
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == "POST" and "survey" in request.data:
            # Allow anonymous responses for public surveys
            survey_id = request.data.get("survey")
            try:
                from src.surveys.models import Survey

                survey = Survey.objects.get(id=survey_id)
                return survey.visibility == "PU" or request.user.is_authenticated
            except Survey.DoesNotExist:
                return False

        return request.user.is_authenticated


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read-only permissions are allowed for any request.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner.
        return hasattr(obj, "created_by") and obj.created_by == request.user


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Allow read-only access to everyone, but write access to staff only.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
