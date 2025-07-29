from core.permissions import (
    IsOwnerOrReadOnly,
    IsPublicResourceOrAuthenticated,
    IsResourceCreator,
)
from rest_framework import permissions


class IsSurveyOwnerOrReadOnly(IsOwnerOrReadOnly):
    """
    Custom permission to only allow owners of a survey to edit it,
    with additional support for survey-specific relationships.
    """

    def has_object_permission(self, request, view, obj):
        # First check with parent class implementation
        if super().has_object_permission(request, view, obj):
            return True

        # Add survey-specific relationship check
        # For nested objects within a survey
        if hasattr(obj, "survey") and hasattr(obj.survey, "created_by"):
            return obj.survey.created_by == request.user

        return False


class IsSurveyCreator(IsResourceCreator):
    """
    Permission to allow only survey creators to manage their resources.
    Works with both direct survey ownership and parent-child survey relationships.
    """

    def has_object_permission(self, request, view, obj):
        # First check with parent class implementation
        if super().has_object_permission(request, view, obj):
            return True

        # Add survey-specific relationship check
        if hasattr(obj, "survey") and hasattr(obj.survey, "created_by"):
            return obj.survey.created_by == request.user

        return False


class IsPublicSurveyOrAuthenticated(IsPublicResourceOrAuthenticated):
    """
    Allow anonymous access to public surveys, but require authentication for private ones.
    """

    public_visibility_code = "PU"  # Survey-specific public code

    def check_public_visibility(self, obj):
        # Direct visibility check for surveys
        if hasattr(obj, "visibility"):
            return obj.visibility == self.public_visibility_code

        # Check parent survey for nested resources
        if hasattr(obj, "survey") and hasattr(obj.survey, "visibility"):
            return obj.survey.visibility == self.public_visibility_code

        return False


class IsAuthenticatedOrReadOnlyForPublicSurveys(permissions.BasePermission):
    """
    Allow anonymous users to respond to public surveys
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow anonymous POST for public/anonymous surveys
        if request.method == "POST":
            survey_id = request.data.get("survey")
            # Try to get survey_pk from URL if not in data
            if not survey_id and hasattr(view, "kwargs"):
                survey_id = view.kwargs.get("survey_pk")
            if survey_id:
                try:
                    from surveys.models import Survey

                    survey = Survey.objects.get(id=survey_id)
                    return survey.visibility == "PU" or request.user.is_authenticated
                except Survey.DoesNotExist:
                    return False
        return request.user.is_authenticated
