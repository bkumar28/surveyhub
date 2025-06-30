from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from common_config.api_message import REQUIRED_FIELD, EXTRA_FIELD_CONTAIN
from survey.models.question import Question


class QuestionViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'title', 'field_type', 'is_required')
        read_only_fields = fields


class QuestionBulkActionSerializer(serializers.ListSerializer):
    def create_question(self, validated_data, surveyObj):
        """
         Create survey question
        :param validated_data:
        :param surveyObj:
        :return:
        """
        for questionDataObj in validated_data:
            # set survey object
            questionDataObj['survey_id'] = surveyObj

            # create question
            Question.objects.create(**questionDataObj)

    def batch_question_func(self, validated_data, surveyObj):
        """
         This function will validate the question action type and perform the operations according.
         it will perform add, update and delete actions.
        :param validated_data:
        :param surveyObj:
        :return:
        """
        for questionDataObj in validated_data:

            if "action_type" in questionDataObj and questionDataObj['action_type'] == "DELETE":
                # delete survey question
                questionDataObj['id'].delete()
                continue

            elif "action_type" in questionDataObj and questionDataObj['action_type'] == "POST":
                del questionDataObj['action_type']
                
                # add new survey question
                self.create_question([questionDataObj], surveyObj)
                continue

            if "action_type" in questionDataObj:
                del questionDataObj['action_type']

            instance = questionDataObj.pop("id")

            for key, value in questionDataObj.items():
                setattr(instance, key, value)

            instance.save()


class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('title', 'field_type', 'is_required', )
        list_serializer_class = QuestionBulkActionSerializer


class QuestionCreateUpdateDeleteSerializer(serializers.ModelSerializer):
    ACTION_TYPE_CHOICE = (
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('DELETE', 'DELETE'),
    )

    id = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    action_type = serializers.ChoiceField(choices=ACTION_TYPE_CHOICE, required=True)

    class Meta:
        model = Question
        fields = ('id', 'title', 'field_type', 'is_required', 'action_type',)
        list_serializer_class = QuestionBulkActionSerializer

    def validate(self, attrs):
        errors = {}

        if "action_type" not in attrs:
            errors.setdefault("action_type", []).append(REQUIRED_FIELD)

        if "action_type" in attrs:
            if attrs['action_type'] == 'POST':
                if "title" not in attrs:
                    errors.setdefault("title", []).append(REQUIRED_FIELD)

                if "field_type" not in attrs:
                    errors.setdefault("field_type", []).append(REQUIRED_FIELD)

                if "id" in attrs:
                    errors.setdefault("id", []).append(EXTRA_FIELD_CONTAIN)

            elif attrs['action_type'] in ['PUT', 'DELETE']:
                if "id" not in attrs:
                    errors.setdefault("id", []).append(REQUIRED_FIELD)
        if errors:
            raise ValidationError(errors)

        return attrs
