import logging

from core.api_message import (
    NOT_FOUND_SURVEY_ERROR,
    REQUEST_PAYLOAD_ERROR,
    SURVEY_RESPONSE_CREATE_SUCCESS,
    SURVEY_RESPONSE_DELETE_SUCCESS,
    SURVEY_RESPONSE_UPDATE_SUCCESS,
)
from core.http_ import Http404
from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from surveys.api.v1.serializers.survey import SurveyResponseSerializer
from surveys.models.survey import Survey, SurveyResponse, SurveyStatus
from surveys.permissions import IsSurveyOwnerOrReadOnly as IsOwnerOrReadOnly

logger = logging.getLogger(__name__)


class SurveyResponseViewSet(viewsets.ModelViewSet):
    serializer_class = SurveyResponseSerializer
    lookup_field = "pk"

    def get_permissions(self):
        """
        Allow anyone to create survey responses (AllowAny for create)
        Owners can view, update, and delete their own responses
        Survey creators can view all responses to their surveys
        """
        if self.action == "create":
            # Allow anonymous users to create responses
            return [AllowAny()]
        elif self.action in ["update", "partial_update", "destroy"]:
            if self.request.user and (
                self.request.user.is_staff or self.request.user.is_superuser
            ):
                return [IsAuthenticatedOrReadOnly()]
            return [IsAuthenticatedOrReadOnly(), IsOwnerOrReadOnly()]
        else:  # list, retrieve, etc.
            return [IsAuthenticatedOrReadOnly()]

    def get_survey(self):
        """
        Get the parent survey for this response
        """
        survey_pk = self.kwargs.get("survey_pk")
        try:
            return Survey.objects.get(pk=survey_pk)
        except Survey.DoesNotExist as err:
            raise Http404(
                message=NOT_FOUND_SURVEY_ERROR.format(survey_pk),
                error_code=status.HTTP_404_NOT_FOUND,
            ) from err

    def get_queryset(self):
        """
        Return all survey responses for detail views (to allow proper 403 responses)
        but filter for list views based on permissions
        """
        survey_pk = self.kwargs.get("survey_pk")
        user = self.request.user

        # For detail views (retrieve/update/destroy), return matching responses
        # This allows proper permission checking to return 403 instead of 404
        if self.action in ["retrieve", "update", "partial_update", "destroy"]:
            return SurveyResponse.objects.filter(survey_id=survey_pk).order_by(
                "-started_at", "id"
            )

        # For list views, apply permission-based filtering
        # Add default ordering to prevent UnorderedObjectListWarning in pagination
        base_qs = SurveyResponse.objects.filter(survey_id=survey_pk).order_by(
            "-started_at", "id"
        )

        # Apply permission-based filtering
        if user.is_authenticated:
            if not (user.is_staff or user.is_superuser):
                # Normal users can only see responses for their own surveys
                base_qs = base_qs.filter(survey__created_by=user)
        else:
            # Anonymous users - no access to responses in most cases
            return SurveyResponse.objects.none()

        return base_qs

    def list(self, request, *args, **kwargs):
        """
        List responses for a survey with custom response format
        """
        # Get filtered queryset
        queryset = self.filter_queryset(self.get_queryset())

        # Handle pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # No pagination
        serializer = self.get_serializer(queryset, many=True)

        # Return formatted response
        return Response(
            {"data": serializer.data, "status": "success", "code": status.HTTP_200_OK}
        )

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific response with custom response format
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # Return formatted response
        return Response(
            {"data": serializer.data, "status": "success", "code": status.HTTP_200_OK}
        )

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        Create a new survey response with custom response format
        """
        # Get the parent survey
        survey = self.get_survey()

        # Check if survey is active
        if survey.status != SurveyStatus.ACTIVE:
            return Response(
                {
                    "details": {
                        "survey": f"Survey is not active, current status: {survey.get_status_display()}"
                    },
                    "message": "Cannot respond to an inactive survey",
                    "status": "failed",
                    "code": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create serializer with survey context
        serializer = self.get_serializer(
            data=request.data, context={"request": request, "view": self}
        )

        # Validate data
        if not serializer.is_valid():
            return Response(
                {
                    "details": serializer.errors,
                    "message": REQUEST_PAYLOAD_ERROR,
                    "status": "failed",
                    "code": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check for missing required answers
        answers_data = request.data.get("answers", [])
        required_questions = survey.questions.filter(is_required=True)

        # If there are required questions but no answers provided
        if required_questions.exists() and not answers_data:
            return Response(
                {
                    "details": {
                        "answers": "This survey contains required questions that must be answered"
                    },
                    "message": "Missing required answers",
                    "status": "failed",
                    "code": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get savepoint for potential rollback
        sid = transaction.savepoint()

        try:
            serializer.save()
        except Exception as err:
            # Rollback transaction on error
            transaction.savepoint_rollback(sid)
            logger.error(f"Error creating response: {str(err)}")
            return Response(
                {
                    "message": str(err),
                    "status": "failed",
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Return success response
        return Response(
            {
                "message": SURVEY_RESPONSE_CREATE_SUCCESS,
                "status": "success",
                "code": status.HTTP_201_CREATED,
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """
        Update a response with custom response format
        """
        instance = self.get_object()

        # Create serializer with instance
        serializer = self.get_serializer(
            instance, data=request.data, partial=False, context={"request": request}
        )

        # Validate data
        if not serializer.is_valid():
            return Response(
                {
                    "details": serializer.errors,
                    "message": REQUEST_PAYLOAD_ERROR,
                    "status": "failed",
                    "code": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get savepoint for potential rollback
        sid = transaction.savepoint()

        try:
            instance = serializer.save()
        except Exception as err:
            # Rollback transaction on error
            transaction.savepoint_rollback(sid)
            logger.error(f"Error updating response: {str(err)}")
            return Response(
                {
                    "message": str(err),
                    "status": "failed",
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Return success response
        return Response(
            {
                "message": SURVEY_RESPONSE_UPDATE_SUCCESS,
                "status": "success",
                "code": status.HTTP_200_OK,
                "data": serializer.data,
            }
        )

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update a response with custom response format
        """
        instance = self.get_object()

        # Create serializer with instance
        serializer = self.get_serializer(
            instance, data=request.data, partial=True, context={"request": request}
        )

        # Validate data
        if not serializer.is_valid():
            return Response(
                {
                    "details": serializer.errors,
                    "message": REQUEST_PAYLOAD_ERROR,
                    "status": "failed",
                    "code": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get savepoint for potential rollback
        sid = transaction.savepoint()

        try:
            instance = serializer.save()
        except Exception as err:
            # Rollback transaction on error
            transaction.savepoint_rollback(sid)
            logger.error(f"Error updating response: {str(err)}")
            return Response(
                {
                    "message": str(err),
                    "status": "failed",
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Return success response
        return Response(
            {
                "message": SURVEY_RESPONSE_UPDATE_SUCCESS,
                "status": "success",
                "code": status.HTTP_200_OK,
                "data": serializer.data,
            }
        )

    def destroy(self, request, *args, **kwargs):
        """
        Delete a response with custom response format
        """
        instance = self.get_object()

        try:
            instance.delete()
        except Exception as err:
            logger.error(f"Error deleting response: {str(err)}")
            return Response(
                {
                    "message": str(err),
                    "status": "failed",
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Return success response
        return Response(
            {
                "message": SURVEY_RESPONSE_DELETE_SUCCESS,
                "status": "success",
                "code": status.HTTP_204_NO_CONTENT,
            },
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(detail=False, methods=["get"], url_path="analytics")
    def analytics(self, request, survey_pk=None):
        """
        Return analytics for the survey responses
        """
        # Get the survey
        try:
            survey = self.get_survey()
        except Http404 as err:
            return Response({"error": err.message}, status=err.error_code)

        # Calculate analytics
        total_responses = SurveyResponse.objects.filter(survey=survey).count()
        completed_responses = SurveyResponse.objects.filter(
            survey=survey, is_complete=True
        ).count()
        completion_rate = (
            round((completed_responses / total_responses) * 100, 2)
            if total_responses > 0
            else 0.0
        )

        analytics_data = {
            "total_responses": total_responses,
            "completed_responses": completed_responses,
            "completion_rate": completion_rate,
        }

        # Return formatted response
        return Response(
            {"data": analytics_data, "status": "success", "code": status.HTTP_200_OK}
        )
