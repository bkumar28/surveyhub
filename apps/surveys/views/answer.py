from django.db import transaction
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
import logging

from common_config.http_ import Http404, HttpError
from common_config.pagination import CustomPagination
from common_config.api_message import REQUEST_PAYLOAD_ERROR, NOT_FOUND_SURVEY_ERROR, EXPIRED_SURVEY_ERROR, \
    NOT_AVAILABLE_SURVEY_ERROR, SURVEY_FORM_SUBMIT_SUCCESS, NOT_FOUND_SURVEY_ANSWER_UUID_ERROR
from survey.models.answer import Answer

from survey.models.survey import Survey
from survey.serializers.answer import SurveyQuestionAnswerSubmitSerializer, SurveyQuestionAnswerViewSerializer

logger = logging.getLogger(__name__)


class AnswerListCreateView(ListCreateAPIView):
    """
    An Api View which provides a method to add new answer or view list answer.
    Returns the success/fail message.
    """
    queryset = Survey.objects.all()
    serializer_class = SurveyQuestionAnswerSubmitSerializer
    pagination_class = CustomPagination
    lookup_field = 'pk'

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}

        try:
            obj = queryset.get(**filter_kwargs)
        except Survey.DoesNotExist:
            raise Http404(message=NOT_FOUND_SURVEY_ERROR.format(self.kwargs['pk']),
                          error_code=status.HTTP_404_NOT_FOUND)
        except Exception as err:
            raise HttpError(message=err.args[0], error_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if obj.status == "D" or obj.start_date > timezone.now():
            raise HttpError(message=NOT_AVAILABLE_SURVEY_ERROR, error_code=status.HTTP_409_CONFLICT)

        elif obj.expired_date < timezone.now():
            raise HttpError(message=EXPIRED_SURVEY_ERROR, error_code=status.HTTP_409_CONFLICT)

        return obj

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = SurveyQuestionAnswerViewSerializer(page, many=True)

            return self.get_paginated_response(serializer.data)

        serializer = SurveyQuestionAnswerViewSerializer(queryset, many=True)

        return Response({"data": serializer.data, "status": "success", "code": status.HTTP_200_OK})

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """
        In this method validate survey from data and submit new answer.
        return success/error message.
        """
        # validate and get survey object
        surveyObj = self.get_object()

        # create survey answer serializers object
        serializer = self.serializer_class(data=request.data, context={'request': request, 'surveyObj': surveyObj})

        # check survey answer serializers is valid
        if not serializer.is_valid():
            return Response({"details": serializer.errors, 'message': REQUEST_PAYLOAD_ERROR, "status": "failed",
                             "code": status.HTTP_400_BAD_REQUEST})

        # get last transaction save point id
        sid = transaction.savepoint()

        try:
            # submit survey answer
            ans_uuid = serializer.create(serializer.validated_data)
        except Exception as err:
            # roll back transaction if any exception occur while submit survey answer
            transaction.savepoint_rollback(sid)
            logger.info("Unexpected error occurred :  %s.", err.args[0])
            return Response({'message': err.args[0], "status": "failed", "code": status.HTTP_500_INTERNAL_SERVER_ERROR})

        # convert model instance into json object
        data = SurveyQuestionAnswerViewSerializer(surveyObj,
                                                  context={'answersListObj': Answer.objects.filter(uuid=ans_uuid)}).data

        return Response({'message': SURVEY_FORM_SUBMIT_SUCCESS, "status": "success", "code": status.HTTP_200_OK,
                         "data": data})


class AnswerRetrieveView(RetrieveAPIView):
    """
    An Api View which provides a method to get, update and delete survey.
    Returns the success/fail message.
    """
    queryset = Answer.objects.all()
    serializer_class = SurveyQuestionAnswerViewSerializer
    lookup_field = ('survey_id', 'uuid',)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        filter_kwargs = {'uuid': self.kwargs['uuid'], 'survey_id': self.kwargs['survey_id']}

        try:
            answersListObj = queryset.filter(**filter_kwargs).order_by("id")
        except Exception as err:
            raise HttpError(message=err.args[0], error_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not answersListObj:
            raise Http404(message=NOT_FOUND_SURVEY_ANSWER_UUID_ERROR.format(self.kwargs['survey_id'],
                                                                            self.kwargs['uuid']),
                          error_code=status.HTTP_404_NOT_FOUND)

        return answersListObj

    def get(self, request, *args, **kwargs):
        # get survey object
        answersListObj = self.get_object()

        try:
            # serialize survey answer json data
            data = self.serializer_class(answersListObj[0].survey_id, context={'answersListObj': answersListObj}).data
        except Exception as err:
            logger.info("Unexpected error occurred :  %s.", err.args[0])
            return Response({'message': err.args[0], "status": "failed",
                             "code": status.HTTP_500_INTERNAL_SERVER_ERROR})

        return Response({"data": data, "status": "success", "code": status.HTTP_200_OK})
