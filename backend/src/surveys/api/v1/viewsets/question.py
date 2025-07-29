import logging

from core.api_message import (
    NOT_FOUND_SURVEY_ERROR,
    REQUEST_PAYLOAD_ERROR,
    SURVEY_QUESTION_CREATE_SUCCESS,
    SURVEY_QUESTION_DELETE_SUCCESS,
    SURVEY_QUESTION_UPDATE_SUCCESS,
)
from core.http_ import Http404
from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from surveys.api.v1.serializers.question import QuestionSerializer
from surveys.models.question import Question
from surveys.models.survey import Survey
from surveys.permissions import IsSurveyCreator

logger = logging.getLogger(__name__)


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    lookup_field = "pk"

    def get_permissions(self):
        """
        Return appropriate permissions:
        - List/Retrieve: Allow any authenticated or read-only access
        - Create: Must be authenticated (survey creator)
        - Update/Delete: Must be authenticated and be the survey creator
        """
        if self.action == "list":
            return [IsAuthenticatedOrReadOnly()]
        elif self.action == "retrieve":
            return [IsAuthenticatedOrReadOnly()]
        elif self.action == "create":
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update", "destroy"]:
            if self.request.user and (
                self.request.user.is_staff or self.request.user.is_superuser
            ):
                return [IsAuthenticated()]
            return [IsAuthenticated(), IsSurveyCreator()]
        return [IsAuthenticatedOrReadOnly()]

    def get_survey(self):
        """
        Get the parent survey for this question
        """
        survey_pk = self.kwargs.get("survey_pk")
        try:
            return Survey.objects.get(pk=survey_pk)
        except Survey.DoesNotExist:
            raise Http404(
                message=NOT_FOUND_SURVEY_ERROR.format(survey_pk),
                error_code=status.HTTP_404_NOT_FOUND,
            )

    def get_queryset(self):
        """
        Return all questions for detail views (to allow proper 403 responses)
        but filter for list views based on permissions
        """
        survey_pk = self.kwargs.get("survey_pk")
        user = self.request.user

        # For detail views (retrieve/update/destroy), return all matching questions
        # This allows proper permission checking to return 403 instead of 404
        if self.action in ["retrieve", "update", "partial_update", "destroy"]:
            return Question.objects.filter(survey_id=survey_pk).order_by("order", "id")

        # For list views, apply permission-based filtering
        # Add default ordering to prevent UnorderedObjectListWarning in pagination
        base_qs = Question.objects.filter(survey_id=survey_pk).order_by("order", "id")

        # Apply permission-based filtering
        if user.is_authenticated:
            if not (user.is_staff or user.is_superuser):
                # For authenticated non-admin users, only return questions from surveys they created
                base_qs = base_qs.filter(survey__created_by=user)
        else:
            # For anonymous users, only return questions from public surveys
            base_qs = base_qs.filter(survey__visibility="PU")

        return base_qs

    def list(self, request, *args, **kwargs):
        """
        List questions for a survey with custom response format
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
        Retrieve a specific question with custom response format
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
        Create a new question with custom response format
        """
        # Get the parent survey
        survey = self.get_survey()

        # Create serializer with survey context
        serializer = self.get_serializer(
            data=request.data, context={"request": request, "survey": survey}
        )

        # Validate data
        if not serializer.is_valid():
            return Response(
                {
                    "details": serializer.errors,
                    "message": REQUEST_PAYLOAD_ERROR,
                    "status": "failed",
                    "code": status.HTTP_400_BAD_REQUEST,
                }
            )

        # Get savepoint for potential rollback
        sid = transaction.savepoint()

        try:
            # Set the survey before saving
            serializer.validated_data["survey"] = survey
            serializer.save()
        except Exception as err:
            # Rollback transaction on error
            transaction.savepoint_rollback(sid)
            logger.error(f"Error creating question: {str(err)}")
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
                "message": SURVEY_QUESTION_CREATE_SUCCESS,
                "status": "success",
                "code": status.HTTP_201_CREATED,
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """
        Update a question with custom response format
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
            logger.error(f"Error updating question: {str(err)}")
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
                "message": SURVEY_QUESTION_UPDATE_SUCCESS,
                "status": "success",
                "code": status.HTTP_200_OK,
                "data": serializer.data,
            }
        )

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update a question with custom response format
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
            logger.error(f"Error updating question: {str(err)}")
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
                "message": SURVEY_QUESTION_UPDATE_SUCCESS,
                "status": "success",
                "code": status.HTTP_200_OK,
                "data": serializer.data,
            }
        )

    def destroy(self, request, *args, **kwargs):
        """
        Delete a question with custom response format
        """
        instance = self.get_object()

        try:
            instance.delete()
        except Exception as err:
            logger.error(f"Error deleting question: {str(err)}")
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
                "message": SURVEY_QUESTION_DELETE_SUCCESS,
                "status": "success",
                "code": status.HTTP_204_NO_CONTENT,
            },
            status=status.HTTP_204_NO_CONTENT,
        )
