from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Avg

from .models.survey import Survey


@shared_task
def send_survey_invitation(invitation_id):
    """Send survey invitation email"""
    from notifications.models import Notification, NotificationTemplate

    try:
        invitation = Notification.objects.get(id=invitation_id)

        subject = f"You're invited to participate in: {invitation.survey.title}"
        message = f"""
        Hello,

        You've been invited to participate in a survey: {invitation.survey.title}

        {invitation.survey.description}

        Click the link below to start the survey:
        {settings.FRONTEND_URL}/survey/{invitation.survey.id}?token={invitation.token}

        Thank you for your time!
        """

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[invitation.email],
            fail_silently=False,
        )

        # Log notification
        NotificationTemplate.objects.create(
            recipient_email=invitation.email,
            subject=subject,
            message=message,
            status="S",
        )

    except Exception as e:
        # Log failed notification
        NotificationTemplate.objects.create(
            recipient_email=invitation.email,
            subject=subject,
            message=message,
            status="F",
            error_message=str(e),
        )


@shared_task
def send_survey_reminders():
    """Send reminders for pending survey invitations"""
    from datetime import timedelta

    from django.utils import timezone
    from notifications.models import Notification

    # Get invitations that haven't been responded to and are older than 3 days
    cutoff_date = timezone.now() - timedelta(days=3)
    pending_invitations = Notification.objects.filter(
        responded_at__isnull=True,
        invited_at__lt=cutoff_date,
        reminder_sent__lt=2,  # Max 2 reminders
    )

    for invitation in pending_invitations:
        if invitation.survey.is_active:
            send_survey_invitation.delay(invitation.id)
            invitation.reminder_sent += 1
            invitation.save()


@shared_task
def update_survey_analytics():
    """Update survey analytics data"""
    from analytics.models import SurveyAnalytics

    for survey in Survey.objects.filter(status="A"):
        analytics, created = SurveyAnalytics.objects.get_or_create(survey=survey)

        total_responses = survey.responses.count()
        completed_responses = survey.responses.filter(is_complete=True).count()

        analytics.total_responses = total_responses
        analytics.completed_responses = completed_responses

        if total_responses > 0:
            analytics.abandonment_rate = (
                (total_responses - completed_responses) / total_responses
            ) * 100

        # Calculate average completion time
        completed_times = survey.responses.filter(
            is_complete=True, completion_time__isnull=False
        ).aggregate(avg_time=Avg("completion_time"))

        analytics.avg_completion_time = completed_times["avg_time"]
        analytics.save()
