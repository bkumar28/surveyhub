import logging

from core.api_message import (
    NOT_FOUND_SURVEY_ERROR,
    NOT_STARTED_SURVEY_YET,
    REQUEST_PAYLOAD_ERROR,
    SURVEY_CREATE_SUCCESS,
    SURVEY_DELETE_SUCCESS,
    SURVEY_UPDATE_SUCCESS,
)
from core.http_ import Http404, HttpError
from core.pagination import CustomPagination
from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.generics import (
    RetrieveAPIView,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from surveys.api.v1.serializers.survey import (
    SurveyCreateSerializer,
    SurveyReportSerializer,
    SurveyViewSerializer,
)
from surveys.models.survey import Survey
from surveys.permissions import IsSurveyOwnerOrReadOnly as IsOwnerOrReadOnly

logger = logging.getLogger(__name__)


class SurveyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination

    def get_queryset(self):
        """
        Return all surveys for detail views (to allow proper 403 responses)
        but filter for list views based on permissions
        """
        user = self.request.user

        # For detail views (retrieve/update/destroy), return all surveys
        # This allows proper permission checking to return 403 instead of 404
        if self.action in ["retrieve", "update", "partial_update", "destroy"]:
            return Survey.objects.all().order_by("-created_at", "id")

        # For list view, apply filtering based on permissions
        qs = Survey.objects.all().order_by("-created_at", "id")

        # Handle authenticated users
        if user.is_authenticated:
            # Only staff/superuser can see all surveys
            if not (user.is_staff or user.is_superuser):
                qs = qs.filter(created_by=user)
        # Anonymous users can only see public surveys
        else:
            qs = qs.filter(visibility="PU")

        # Support filtering by status/visibility
        status_param = self.request.query_params.get("status")
        if status_param:
            qs = qs.filter(status=status_param)
        visibility_param = self.request.query_params.get("visibility")
        if visibility_param:
            qs = qs.filter(visibility=visibility_param)

        return qs

    def get_permissions(self):
        # Allow admin/staff to update/delete any survey
        if self.action in ["update", "partial_update", "destroy"]:
            if self.request.user and (
                self.request.user.is_staff or self.request.user.is_superuser
            ):
                return [IsAuthenticatedOrReadOnly()]
            return [IsAuthenticatedOrReadOnly(), IsOwnerOrReadOnly()]
        return [IsAuthenticatedOrReadOnly()]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return SurveyCreateSerializer
        return SurveyViewSerializer

    def list(self, request, *args, **kwargs):
        """
        List surveys with custom response format
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
        Retrieve a specific survey with custom response format
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
        Create a new survey with custom response format
        """
        # Create serializer with data
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
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
            # Save the new survey
            instance = serializer.save()

            # Use SurveyViewSerializer for response
            view_serializer = SurveyViewSerializer(
                instance, context={"request": request}
            )
        except Exception as err:
            # Rollback transaction on error
            transaction.savepoint_rollback(sid)
            logger.error(f"Error creating survey: {str(err)}")
            return Response(
                {
                    "message": str(err),
                    "status": "failed",
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Return success response
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "message": SURVEY_CREATE_SUCCESS,
                "status": "success",
                "code": status.HTTP_201_CREATED,
                "data": view_serializer.data,
            },
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """
        Update a survey with custom response format
        """
        instance = self.get_object()

        # Create serializer with instance
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=False,
            context={"request": request, "surveyObj": instance},
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
            # Save the updated survey
            instance = serializer.save()

            # Use SurveyViewSerializer for response
            view_serializer = SurveyViewSerializer(
                instance, context={"request": request}
            )
        except Exception as err:
            # Rollback transaction on error
            transaction.savepoint_rollback(sid)
            logger.error(f"Error updating survey: {str(err)}")
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
                "message": SURVEY_UPDATE_SUCCESS,
                "status": "success",
                "code": status.HTTP_200_OK,
                "data": view_serializer.data,
            }
        )

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update a survey with custom response format
        """
        instance = self.get_object()

        # Create serializer with instance
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True,
            context={"request": request, "surveyObj": instance},
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
            # Save the updated survey
            instance = serializer.save()

            # Use SurveyViewSerializer for response
            view_serializer = SurveyViewSerializer(
                instance, context={"request": request}
            )
        except Exception as err:
            # Rollback transaction on error
            transaction.savepoint_rollback(sid)
            logger.error(f"Error updating survey: {str(err)}")
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
                "message": SURVEY_UPDATE_SUCCESS,
                "status": "success",
                "code": status.HTTP_200_OK,
                "data": view_serializer.data,
            }
        )

    def destroy(self, request, *args, **kwargs):
        """
        Delete a survey with custom response format
        """
        instance = self.get_object()

        try:
            instance.delete()
        except Exception as err:
            logger.error(f"Error deleting survey: {str(err)}")
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
                "message": SURVEY_DELETE_SUCCESS,
                "status": "success",
                "code": status.HTTP_204_NO_CONTENT,
            },
            status=status.HTTP_204_NO_CONTENT,
        )


class SurveyReportView(RetrieveAPIView):
    """
    An Api View which provides a method to get survey report.
    Returns the success/fail message.
    """

    queryset = Survey.objects.all()
    serializer_class = SurveyReportSerializer
    lookup_field = "pk"

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}

        try:
            obj = queryset.get(**filter_kwargs)
        except Survey.DoesNotExist as err:
            raise Http404(
                message=NOT_FOUND_SURVEY_ERROR.format(self.kwargs["pk"]),
                error_code=status.HTTP_404_NOT_FOUND,
            ) from err
        except Exception as err:
            raise HttpError(
                message=str(err), error_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) from err

        if obj.status == "D":
            raise HttpError(
                message=NOT_STARTED_SURVEY_YET, error_code=status.HTTP_409_CONFLICT
            )

        return obj

    def get(self, request, *args, **kwargs):
        """
        Get survey report with custom response format
        """
        # Get survey object
        instance = self.get_object()

        try:
            # Get survey report data
            data = self.serializer_class(instance).data
        except Exception as err:
            logger.error(f"Error fetching survey report: {str(err)}")
            return Response(
                {
                    "message": str(err),
                    "status": "failed",
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Return formatted response
        return Response({"data": data, "status": "success", "code": status.HTTP_200_OK})
