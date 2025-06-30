from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from common_config.api_message import QUESTION_MAX_LIMIT, INVALID_SURVEY_START_DATE, INVALID_SURVEY_EXPIRED_DATE, \
    INVALID_SURVEY_EXPIRED_FUTURE_DATE, REQUIRED_FIELD, START_DATE_MUST_LESS_THAN_EXPIRED_DATE
from survey.models.survey import Survey, SurveyInvitation
from survey.serializers.common import UserViewSerializer
from survey.serializers.question import QuestionCreateSerializer, QuestionViewSerializer, \
    QuestionCreateUpdateDeleteSerializer


class SurveyReportSerializer(serializers.ModelSerializer):
    reports = serializers.SerializerMethodField('get_reports')

    class Meta:
        model = Survey
        fields = ('id', 'title', 'description', 'start_date', 'expired_date', 'status', "reports")
        read_only_fields = fields

    def get_reports(self, value):
        # get all survey answer
        answers = value.answers.all()

        # get top popular answer object
        popularAnswer = answers.filter(~Q(ans='')).values("question_id__title").annotate(
                                        total=Count('question_id')).order_by('-total')[:1]

        # get top unpopular answer object
        unpopularAnswer = answers.filter(ans='').values("question_id__title").annotate(
                                    total=Count('question_id')).order_by('-total')[:1]

        data = dict(total_submission=answers.values("uuid").distinct().count(),
                    anonymous_user=answers.filter(invitation_id__isnull=True).values("uuid").distinct().count(),
                    invited_user=answers.filter(invitation_id__isnull=False).values("uuid").distinct().count(),
                    total_answer=answers.filter(~Q(ans='')).count(),
                    total_unanswer=answers.filter(ans='').count(),
                    popular_answer={'total': 0, 'question': ''},
                    unpopular_answer={'total': 0, 'question': ''})

        if popularAnswer:
            data['popular_answer']['total'] = popularAnswer[0]['total']
            data['popular_answer']['question'] = popularAnswer[0]['question_id__title']

        if unpopularAnswer:
            data['unpopular_answer']['total'] = unpopularAnswer[0]['total']
            data['unpopular_answer']['question'] = unpopularAnswer[0]['question_id__title']

        return data


class SurveyViewSerializer(serializers.ModelSerializer):
    questions = QuestionViewSerializer(many=True)

    class Meta:
        model = Survey
        fields = ('id', 'title', 'description', 'start_date', 'expired_date', 'status', 'created_by', 'updated_by',
                  'created_on', 'updated_on', "questions",)
        read_only_fields = fields


class SurveyInvitationViewSerializer(serializers.ModelSerializer):
    user = UserViewSerializer(source="user_id")
    survey = SurveyViewSerializer(source="survey_id")

    class Meta:
        model = SurveyInvitation
        fields = ('id', "email", "user", "survey",)
        read_only_fields = fields


class SurveyCreateSerializer(serializers.ModelSerializer):
    questions = QuestionCreateSerializer(many=True, read_only=False, allow_null=False, required=False)

    class Meta:
        model = Survey
        fields = ('title', 'description', 'start_date', 'expired_date', 'status', "questions",)

    def validate(self, attrs):
        errors = {}

        if "questions" in attrs and len(attrs['questions']) > 10:
            errors.setdefault("questions", []).append(QUESTION_MAX_LIMIT)

        if "start_date" in attrs and attrs['start_date'] is not None and attrs['start_date'] <= timezone.now():
            errors.setdefault("start_date", []).append(INVALID_SURVEY_START_DATE)

        if "expired_date" in attrs and attrs['expired_date'] is not None and attrs['expired_date'] < timezone.now():
            errors.setdefault("expired_date", []).append(INVALID_SURVEY_EXPIRED_FUTURE_DATE)

        if "start_date" in attrs and "start_date" in attrs and attrs['expired_date'] is not None and attrs[
            'expired_date'] \
                is not None:
            if attrs['expired_date'] <= attrs['start_date']:
                errors.setdefault("expired_date", []).append(INVALID_SURVEY_EXPIRED_DATE)

        if errors:
            raise ValidationError(errors)

        return attrs

    def create(self, validated_data):
        questions = validated_data.pop("questions", [])

        # add new survey
        instance = Survey.objects.create(**validated_data)

        if questions:
            self.fields['questions'].create_question(questions, instance)

        return instance


class SurveyUpdateSerializer(serializers.ModelSerializer):
    questions = QuestionCreateUpdateDeleteSerializer(many=True, read_only=False, allow_null=False, required=False)

    class Meta:
        model = Survey
        fields = ('title', 'description', 'start_date', 'expired_date', 'status', "questions",)

    def validate_questions(self, values):
        if values and "surveyObj" in self.context:
            # get all survey questions
            questionCount = self.context['surveyObj'].questions.all().count()

            for xx in values:
                if xx['action_type'] == 'POST':
                    questionCount += 1
                elif xx['action_type'] == 'DELETE':
                    questionCount -= 1

            if questionCount > 10:
                raise ValidationError(QUESTION_MAX_LIMIT)

        return values

    def validate(self, attrs):
        errors = {}

        if "start_date" in attrs and attrs['start_date'] is not None and attrs['start_date'] <= timezone.now():
            errors.setdefault("start_date", []).append(INVALID_SURVEY_START_DATE)

        if "expired_date" in attrs and attrs['expired_date'] is not None:
            # validate expired date
            if 'start_date' not in attrs and self.context['surveyObj'].start_date >= attrs['expired_date']:
                errors.setdefault("expired_date", []).append(INVALID_SURVEY_EXPIRED_FUTURE_DATE)

        if "start_date" in attrs and "start_date" in attrs and attrs['start_date'] is not None:
            # validate start date
            if "expired_date" not in attrs and self.context['surveyObj'].expired_date <= attrs['start_date']:
                errors.setdefault("start_date", []).append(START_DATE_MUST_LESS_THAN_EXPIRED_DATE)

            elif "expired_date" in attrs and attrs['expired_date'] is not None\
                    and attrs['expired_date'] <= attrs['start_date']:
                errors.setdefault("expired_date", []).append(INVALID_SURVEY_EXPIRED_DATE)

        if "status" in attrs and attrs['status'] == 'S':
            if 'start_date' not in attrs and self.context['surveyObj'].start_date <= timezone.now():
                errors.setdefault("start_date", []).append(INVALID_SURVEY_START_DATE)

            if 'expired_date' not in attrs and self.context['surveyObj'].expired_date <= timezone.now():
                errors.setdefault("expired_date", []).append(INVALID_SURVEY_EXPIRED_FUTURE_DATE)

        if errors:
            raise ValidationError(errors)

        return attrs

    def update(self, instance, validated_data):
        questions = validated_data.pop("questions", [])

        if validated_data:
            # set survey fields value
            for key, item in validated_data.items():
                setattr(instance, key, item)

            instance.updated_on = timezone.now()

            # update survey
            instance.save()

        if questions:
            # add/update/delete survey questions
            self.fields['questions'].batch_question_func(questions, instance)

        return instance


class SurveySendSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyInvitation
        fields = ('email', 'user_id',)

    def validate(self, attrs):
        errors = {}

        if "email" not in attrs and "user_id" not in attrs:
            errors.setdefault("email", []).append(REQUIRED_FIELD)

        if errors:
            raise ValidationError(errors)

        return attrs
    
    def create(self, validated_data):
        validated_data['survey_id'] = self.context['surveyObj']
        return super(SurveySendSerializer, self).create(validated_data)