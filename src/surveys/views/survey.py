import logging

from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response

from core.api_message import (
    EXPIRED_SURVEY_ERROR,
    NOT_AVAILABLE_SURVEY_ERROR,
    NOT_FOUND_SURVEY_ERROR,
    NOT_STARTED_SURVEY_YET,
    REQUEST_PAYLOAD_ERROR,
    SURVEY_CREATE_SUCCESS,
    SURVEY_DELETE_SUCCESS,
    SURVEY_SENT_SUCCESS,
    SURVEY_UPDATE_SUCCESS,
)
from core.http_ import Http404, HttpError
from core.pagination import CustomPagination
from surveys.models.survey import Survey
from surveys.serializers.survey import (
    SurveyCreateSerializer,
    SurveyInvitationViewSerializer,
    SurveyReportSerializer,
    SurveySendSerializer,
    SurveyUpdateSerializer,
    SurveyViewSerializer,
)

logger = logging.getLogger(__name__)


class SurveyListCreateView(ListCreateAPIView):
    """
    An Api View which provides a method to add new survey or view list survey.
    Returns the success/fail message.
    """

    queryset = Survey.objects.all()
    serializer_class = SurveyCreateSerializer
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = SurveyViewSerializer(page, many=True)

            return self.get_paginated_response(serializer.data)

        serializer = SurveyViewSerializer(queryset, many=True)

        return Response(
            {"data": serializer.data, "status": "success", "code": status.HTTP_200_OK}
        )

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """
        In this method validate survey from data and created new survey.
        return success/error message.
        """
        # create survey serializers object
        serializer = SurveyCreateSerializer(
            data=request.data, context={"request": request}
        )

        # check survey serializers is valid
        if not serializer.is_valid():
            return Response(
                {
                    "details": serializer.errors,
                    "message": REQUEST_PAYLOAD_ERROR,
                    "status": "failed",
                    "code": status.HTTP_400_BAD_REQUEST,
                }
            )

        # get last transaction save point id
        sid = transaction.savepoint()

        try:
            # add new survey
            instance = serializer.create(serializer.validated_data)
        except Exception as err:
            # roll back transaction if any exception occur while adding survey
            transaction.savepoint_rollback(sid)
            logger.info("Unexpected error occurred :  %s.", err.args[0])
            return Response(
                {
                    "message": err.args[0],
                    "status": "failed",
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                }
            )

        return Response(
            {
                "message": SURVEY_CREATE_SUCCESS,
                "status": "success",
                "code": status.HTTP_201_CREATED,
                "data": SurveyViewSerializer(instance).data,
            }
        )


class SurveyRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    An Api View which provides a method to get, update and delete survey.
    Returns the success/fail message.
    """

    queryset = Survey.objects.all()
    serializer_class = SurveyUpdateSerializer
    lookup_field = "pk"

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}

        try:
            obj = queryset.get(**filter_kwargs)
        except Survey.DoesNotExist:
            raise Http404(
                message=NOT_FOUND_SURVEY_ERROR.format(self.kwargs["pk"]),
                error_code=status.HTTP_404_NOT_FOUND,
            )
        except Exception as err:
            raise HttpError(
                message=err.args[0], error_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return obj

    def get(self, request, *args, **kwargs):
        # get survey object
        instance = self.get_object()

        try:
            # serialize survey objects
            data = SurveyViewSerializer(instance).data
        except Exception as err:
            logger.info("Unexpected error occurred :  %s.", err.args[0])
            return Response(
                {
                    "message": err.args[0],
                    "status": "failed",
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                }
            )

        return Response({"data": data, "status": "success", "code": status.HTTP_200_OK})

    @transaction.atomic
    def put(self, request, *args, **kwargs):
        # get survey object
        instance = self.get_object()

        # create survey serializers object
        serializer = self.serializer_class(
            data=request.data, partial=True, context={"survey_obj": instance}
        )

        # check survey serializers is valid
        if not serializer.is_valid():
            return Response(
                {
                    "details": serializer.errors,
                    "message": REQUEST_PAYLOAD_ERROR,
                    "status": "failed",
                    "code": status.HTTP_400_BAD_REQUEST,
                }
            )

        # get last transaction save point id
        sid = transaction.savepoint()

        try:
            # update survey
            instance = serializer.update(instance, serializer.validated_data)
        except Exception as err:
            logger.info("Unexpected error occurred 2 :  %s.", err.args[0])
            # roll back transaction if any exception occur while updating survey
            transaction.savepoint_rollback(sid)
            return Response(
                {
                    "message": err.args[0],
                    "status": "failed",
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                }
            )

        return Response(
            {
                "message": SURVEY_UPDATE_SUCCESS,
                "status": "success",
                "code": status.HTTP_200_OK,
                "data": SurveyViewSerializer(instance).data,
            }
        )

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        # validate and get survey object
        instance = self.get_object()

        # get last transaction save point id
        sid = transaction.savepoint()

        try:
            # soft delete survey
            instance.delete()
        except Exception as err:
            # roll back transaction if any exception occur while delete survey
            transaction.savepoint_rollback(sid)
            logger.info("Unexpected error occurred :  %s.", err.args[0])
            return Response(
                {
                    "message": err.args[0],
                    "status": "failed",
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                }
            )

        return Response(
            {
                "message": SURVEY_DELETE_SUCCESS,
                "status": "success",
                "code": status.HTTP_204_NO_CONTENT,
            }
        )


class SurveySendView(ListCreateAPIView):
    """
    An Api View which provides a method to send survey invitation.
    Returns the success/fail message.
    """

    queryset = Survey.objects.all()
    serializer_class = SurveySendSerializer
    lookup_field = "pk"

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}

        try:
            obj = queryset.get(**filter_kwargs)
        except Survey.DoesNotExist:
            raise Http404(
                message=NOT_FOUND_SURVEY_ERROR.format(self.kwargs["pk"]),
                error_code=status.HTTP_404_NOT_FOUND,
            )
        except Exception as err:
            raise HttpError(
                message=err.args[0], error_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return obj

    def list(self, request, *args, **kwargs):
        survey_obj = self.get_object()

        queryset = survey_obj.invitation.all()

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = SurveyInvitationViewSerializer(page, many=True)

            return self.get_paginated_response(serializer.data)

        serializer = SurveyInvitationViewSerializer(queryset, many=True)

        return Response(
            {"data": serializer.data, "status": "success", "code": status.HTTP_200_OK}
        )

    def post(self, request, *args, **kwargs):
        # get survey object
        survey_obj = self.get_object()

        if survey_obj.status == "D" or survey_obj.start_date > timezone.now():
            raise HttpError(
                message=NOT_AVAILABLE_SURVEY_ERROR, error_code=status.HTTP_409_CONFLICT
            )

        elif survey_obj.expired_date < timezone.now():
            raise HttpError(
                message=EXPIRED_SURVEY_ERROR, error_code=status.HTTP_409_CONFLICT
            )

        # create send survey invitation serializers object
        serializer = self.serializer_class(
            data=request.data, context={"request": request, "survey_obj": survey_obj}
        )

        # check send survey invitation serializers is valid
        if not serializer.is_valid():
            return Response(
                {
                    "details": serializer.errors,
                    "message": REQUEST_PAYLOAD_ERROR,
                    "status": "failed",
                    "code": status.HTTP_400_BAD_REQUEST,
                }
            )

        # get last transaction save point id
        sid = transaction.savepoint()

        try:
            # send survey invitation
            instance = serializer.create(serializer.validated_data)
        except Exception as err:
            # roll back transaction if any exception occur while send survey invitation
            transaction.savepoint_rollback(sid)
            logger.info("Unexpected error occurred :  %s.", err.args[0])
            return Response(
                {
                    "message": err.args[0],
                    "status": "failed",
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                }
            )

        return Response(
            {
                "message": SURVEY_SENT_SUCCESS,
                "status": "success",
                "code": status.HTTP_200_OK,
                "data": SurveyInvitationViewSerializer(instance).data,
            }
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
        except Survey.DoesNotExist:
            raise Http404(
                message=NOT_FOUND_SURVEY_ERROR.format(self.kwargs["pk"]),
                error_code=status.HTTP_404_NOT_FOUND,
            )
        except Exception as err:
            raise HttpError(
                message=err.args[0], error_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        if obj.status == "D":
            raise HttpError(
                message=NOT_STARTED_SURVEY_YET, error_code=status.HTTP_409_CONFLICT
            )

        return obj

    def get(self, request, *args, **kwargs):
        # get survey object
        instance = self.get_object()

        try:
            #  survey report data
            data = self.serializer_class(instance).data
        except Exception as err:
            logger.info("Unexpected error occurred :  %s.", err.args[0])
            return Response(
                {
                    "message": err.args[0],
                    "status": "failed",
                    "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                }
            )

        return Response({"data": data, "status": "success", "code": status.HTTP_200_OK})
