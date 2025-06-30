import uuid
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from common_config.api_message import REQUIRED_FIELD, INVALID_SURVEY_INVITATION_ID, INVALID_SURVEY_QUESTION_ID, \
    INVALID_ANS_NUMBER_VALUE, NOT_ALLOW_BLANK_VALUE
from survey.models.survey import Survey
from survey.models.answer import Answer
from survey.serializers.common import UserViewSerializer


class AnswerViewSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField('get_question')
    field_type = serializers.SerializerMethodField('get_field_type')
    submitted_by = serializers.SerializerMethodField('get_submitted_by_detail')

    class Meta:
        model = Answer
        fields = ('id', 'question', 'field_type', 'ans', "submit_date", "uuid", "submitted_by",)
        read_only_fields = fields

    def get_question(self, value):
        return value.question_id.title

    def get_field_type(self, value):
        return value.question_id.field_type

    def get_submitted_by_detail(self, value):
        if value.invitation_id is None:
            return {'name': 'Anonymous User'}

        if value.invitation_id.user_id is not None:
            return UserViewSerializer(value.invitation_id.user_id).data

        return {'email': value.invitation_id.email}


class SurveyQuestionAnswerViewSerializer(serializers.ModelSerializer):
    question_ans = serializers.SerializerMethodField('get_qt_ans')

    class Meta:
        model = Survey
        fields = ('id', 'title', 'description', 'start_date', 'expired_date', "question_ans",)
        read_only_fields = fields

    def get_qt_ans(self, value):
        if 'answersListObj' in self.context:
            answersListObj = self.context['answersListObj']
        else:
            answersListObj = value.answers.all().order_by("id")

        return AnswerViewSerializer(answersListObj, many=True).data


class QuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('question_id', 'ans',)

    def validate(self, attrs):
        errors = {}
        if "question_id" not in attrs:
            errors.setdefault("question_id", []).append(REQUIRED_FIELD)

        if "ans" not in attrs:
            errors.setdefault("ans", []).append(REQUIRED_FIELD)

        if "question_id" in attrs and attrs['question_id'] is not None:
            if self.context['surveyObj'].id != attrs['question_id'].survey_id.id:
                errors.setdefault("question_id", []).append(INVALID_SURVEY_QUESTION_ID.format(attrs['question_id'].id))

            elif "ans" in attrs:
                if attrs['question_id'].is_required and "ans" in attrs and attrs['ans'] == "":
                    errors.setdefault("ans", []).append(NOT_ALLOW_BLANK_VALUE)

                elif attrs['question_id'].field_type == 'N' and attrs['ans'] and not attrs['ans'].isdigit():
                    errors.setdefault("ans", []).append(INVALID_ANS_NUMBER_VALUE)
        if errors:
            raise ValidationError(errors)

        return attrs


class SurveyQuestionAnswerSubmitSerializer(serializers.ModelSerializer):
    answers = QuestionAnswerSerializer(many=True, read_only=False, allow_null=False, required=True)

    class Meta:
        model = Answer
        fields = ("answers", "invitation_id",)

    def validate(self, attrs):
        errors = {}

        if "invitation_id" in attrs and attrs['invitation_id'] is not None and \
                self.context['surveyObj'].id != attrs['invitation_id'].survey_id.id:
            errors.setdefault("invitation_id", []).append(INVALID_SURVEY_INVITATION_ID.format(
                attrs['invitation_id'].id))

        if errors:
            raise ValidationError(errors)

        return attrs

    def create(self, validated_data):
        invitation_id = validated_data.pop("invitation_id", None)
        ans_uuid = str(uuid.uuid4().hex)

        for ansDataObj in validated_data['answers']:
            ansDataObj['invitation_id'] = invitation_id
            ansDataObj['uuid'] = ans_uuid
            ansDataObj['survey_id'] = self.context['surveyObj']

            # add survey answer
            Answer.objects.create(**ansDataObj)

        return ans_uuid
