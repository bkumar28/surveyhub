from collections import Counter, defaultdict
from datetime import timedelta

from django.db.models import Avg, Count, F, Max, Min, StdDev
from django.utils import timezone
from surveys.models.answer import Answer


class AnalyticsService:
    """Advanced analytics service for survey data"""

    def __init__(self, survey):
        self.survey = survey

    def get_response_analytics(self):
        """Get comprehensive response analytics"""
        responses = self.survey.responses.all()
        completed_responses = responses.filter(is_complete=True)

        # Basic metrics
        total_responses = responses.count()
        completed_count = completed_responses.count()
        completion_rate = (
            (completed_count / total_responses * 100) if total_responses > 0 else 0
        )

        # Time-based analytics
        avg_completion_time = completed_responses.aggregate(
            avg_time=Avg("completion_time")
        )["avg_time"]

        # Response timeline (last 30 days)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        daily_responses = (
            responses.filter(submitted_at__gte=thirty_days_ago)
            .extra(select={"day": "date(submitted_at)"})
            .values("day")
            .annotate(count=Count("id"))
            .order_by("day")
        )

        # Device/User agent analysis
        user_agents = (
            responses.values("user_agent")
            .annotate(count=Count("id"))
            .order_by("-count")[:10]
        )

        return {
            "total_responses": total_responses,
            "completed_responses": completed_count,
            "completion_rate": round(completion_rate, 2),
            "average_completion_time": avg_completion_time,
            "daily_responses": list(daily_responses),
            "top_user_agents": list(user_agents),
            "abandonment_points": self._get_abandonment_points(),
        }

    def get_question_analytics(self):
        """Get detailed analytics for each question"""
        question_analytics = []

        for question in self.survey.questions.all():
            answers = Answer.objects.filter(question=question)
            total_answers = answers.count()
            total_responses = self.survey.responses.count()

            analytics = {
                "question_id": question.id,
                "question_title": question.title,
                "question_type": question.field_type,
                "total_answers": total_answers,
                "answer_rate": (
                    (total_answers / total_responses * 100)
                    if total_responses > 0
                    else 0
                ),
                "skip_rate": (
                    ((total_responses - total_answers) / total_responses * 100)
                    if total_responses > 0
                    else 0
                ),
            }

            # Type-specific analytics
            if question.field_type == "T":
                analytics.update(self._analyze_text_question(question, answers))
            elif question.field_type == "N":
                analytics.update(self._analyze_number_question(question, answers))
            elif question.field_type in ["SC", "MC"]:
                analytics.update(self._analyze_choice_question(question, answers))
            elif question.field_type == "R":
                analytics.update(self._analyze_rating_question(question, answers))

            question_analytics.append(analytics)

        return question_analytics

    def _analyze_text_question(self, question, answers):
        """Analyze text-based questions"""
        text_answers = answers.filter(text_answer__isnull=False)

        if not text_answers.exists():
            return {"word_cloud": [], "avg_length": 0, "sentiment": None}

        # Word frequency analysis
        all_text = " ".join([answer.text_answer for answer in text_answers])
        words = all_text.lower().split()
        word_freq = Counter(words)
        common_words = word_freq.most_common(20)

        # Average length
        avg_length = (
            text_answers.aggregate(avg_len=Avg(F("text_answer__length")))["avg_len"]
            or 0
        )

        return {
            "word_cloud": common_words,
            "avg_length": round(avg_length, 2),
            "response_lengths": self._get_length_distribution(text_answers),
        }

    def _analyze_number_question(self, question, answers):
        """Analyze numerical questions"""
        number_answers = answers.filter(number_answer__isnull=False)

        if not number_answers.exists():
            return {"statistics": {}, "distribution": []}

        stats = number_answers.aggregate(
            min_val=Min("number_answer"),
            max_val=Max("number_answer"),
            avg_val=Avg("number_answer"),
            std_dev=StdDev("number_answer"),
        )

        # Create distribution buckets
        distribution = self._create_number_distribution(number_answers)

        return {
            "statistics": {
                "min": float(stats["min_val"] or 0),
                "max": float(stats["max_val"] or 0),
                "average": round(float(stats["avg_val"] or 0), 2),
                "std_deviation": round(float(stats["std_dev"] or 0), 2),
            },
            "distribution": distribution,
        }

    def _analyze_choice_question(self, question, answers):
        """Analyze single/multiple choice questions"""
        choice_counts = defaultdict(int)

        for answer in answers:
            if answer.choice_answers:
                for choice in answer.choice_answers:
                    choice_counts[choice] += 1

        # Calculate percentages
        total_answers = sum(choice_counts.values())
        choice_percentages = [
            {
                "option": option,
                "count": count,
                "percentage": (
                    round((count / total_answers * 100), 2) if total_answers > 0 else 0
                ),
            }
            for option, count in choice_counts.items()
        ]

        # Sort by count
        choice_percentages.sort(key=lambda x: x["count"], reverse=True)

        return {
            "choice_distribution": choice_percentages,
            "most_popular": choice_percentages[0] if choice_percentages else None,
            "least_popular": choice_percentages[-1] if choice_percentages else None,
        }

    def _analyze_rating_question(self, question, answers):
        """Analyze rating scale questions"""
        number_answers = answers.filter(number_answer__isnull=False)

        if not number_answers.exists():
            return {"rating_distribution": [], "average_rating": 0}

        # Rating distribution
        rating_counts = (
            number_answers.values("number_answer")
            .annotate(count=Count("id"))
            .order_by("number_answer")
        )

        avg_rating = number_answers.aggregate(avg=Avg("number_answer"))["avg"] or 0

        return {
            "rating_distribution": list(rating_counts),
            "average_rating": round(float(avg_rating), 2),
            "rating_summary": self._get_rating_summary(avg_rating, question.scale_max),
        }

    def _get_abandonment_points(self):
        """Identify where users abandon the survey"""
        questions = self.survey.questions.all().order_by("order")
        abandonment_points = []

        total_responses = self.survey.responses.count()

        for _i, question in enumerate(questions):
            answered_count = Answer.objects.filter(question=question).count()
            abandonment_rate = (
                ((total_responses - answered_count) / total_responses * 100)
                if total_responses > 0
                else 0
            )

            abandonment_points.append(
                {
                    "question_order": question.order,
                    "question_title": question.title,
                    "abandonment_rate": round(abandonment_rate, 2),
                    "answered_count": answered_count,
                }
            )

        return abandonment_points

    def generate_report_data(self):
        """Generate comprehensive report data"""
        return {
            "survey_info": {
                "id": self.survey.id,
                "title": self.survey.title,
                "description": self.survey.description,
                "created_at": self.survey.created_at,
                "status": self.survey.status,
            },
            "response_analytics": self.get_response_analytics(),
            "question_analytics": self.get_question_analytics(),
            "generated_at": timezone.now(),
        }
