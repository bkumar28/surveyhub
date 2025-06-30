from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Survey
from apps.analytics.services import AnalyticsService
from apps.core.cache import CacheService
from apps.notifications.models import SurveyInvitation

@shared_task
def send_survey_invitation(invitation_id):
    try:
        invitation = SurveyInvitation.objects.get(id=invitation_id)
        survey = invitation.survey
        
        subject = f"You're invited to participate in: {survey.title}"
        
        context = {
            'survey': survey,
            'invitation': invitation,
            'survey_url': f"{settings.FRONTEND_URL}/survey/{survey.id}?token={invitation.token}"
        }
        
        html_message = render_to_string('emails/survey_invitation.html', context)
        plain_message = render_to_string('emails/survey_invitation.txt', context)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[invitation.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        invitation.sent_at = timezone.now()
        invitation.save()
        
        return f"Invitation sent to {invitation.email}"
    
    except Exception as e:
        return f"Failed to send invitation: {str(e)}"

@shared_task
def generate_survey_report(survey_id):
    try:
        survey = Survey.objects.get(id=survey_id)
        analytics_service = AnalyticsService()
        
        report_data = analytics_service.generate_comprehensive_report(survey)
        
        # Cache the report
        CacheService.cache_report_data(survey_id, report_data)
        
        return f"Report generated for survey {survey_id}"
    
    except Exception as e:
        return f"Failed to generate report: {str(e)}"

@shared_task
def update_survey_analytics():
    """Periodic task to update analytics for all active surveys"""
    active_surveys = Survey.objects.filter(status='A')
    analytics_service = AnalyticsService()
    
    for survey in active_surveys:
        analytics_service.update_survey_analytics(survey)
    
    return f"Updated analytics for {active_surveys.count()} surveys"

@shared_task
def cleanup_incomplete_responses():
    """Remove incomplete responses older than 24 hours"""
    from datetime import timedelta
    cutoff_time = timezone.now() - timedelta(hours=24)
    
    deleted_count = SurveyResponse.objects.filter(
        is_complete=False,
        started_at__lt=cutoff_time
    ).delete()[0]
    
    return f"Cleaned up {deleted_count} incomplete responses"