import requests
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from twilio.rest import Client  # For SMS notifications


class NotificationService:
    """Handle various types of notifications"""

    def __init__(self):
        self.twilio_client = None
        if hasattr(settings, "TWILIO_ACCOUNT_SID"):
            self.twilio_client = Client(
                settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN
            )

    def send_notification_email(self, notification):
        """Send styled notification email"""
        context = {
            "survey": notification.survey,
            "notification": notification,
            "survey_url": f"{settings.FRONTEND_URL}/survey/{notification.survey.id}"
            + f"?token={notification.token}",
        }

        subject = f"You're invited: {notification.survey.title}"

        # Render HTML email template
        html_content = render_to_string("emails/notification.html", context)
        text_content = render_to_string("emails/notification.txt", context)

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[notification.email],
        )
        email.attach_alternative(html_content, "text/html")

        try:
            email.send()
            return True
        except Exception as e:
            print(f"Email sending failed: {e}")
            return False

    def send_sms_notification(self, phone_number, message):
        """Send SMS notification using Twilio"""
        if not self.twilio_client:
            return False

        try:
            message = self.twilio_client.messages.create(
                body=message, from_=settings.TWILIO_PHONE_NUMBER, to=phone_number
            )
            return True
        except Exception as e:
            print(f"SMS sending failed: {e}")
            return False

    def send_slack_notification(self, webhook_url, message):
        """Send Slack notification"""
        payload = {
            "text": message,
            "username": "SurveyHub Bot",
            "icon_emoji": ":clipboard:",
        }

        try:
            response = requests.post(webhook_url, json=payload)
            return response.status_code == 200
        except Exception as e:
            print(f"Slack notification failed: {e}")
            return False

    def send_survey_completion_notification(self, survey_response):
        """Notify survey owner of new response"""
        survey = survey_response.survey
        owner_email = survey.created_by.email

        context = {
            "survey": survey,
            "response": survey_response,
            "dashboard_url": f"{settings.FRONTEND_URL}/dashboard/surveys/{survey.id}",
        }

        subject = f"New response received: {survey.title}"
        html_content = render_to_string("emails/new_response.html", context)
        text_content = render_to_string("emails/new_response.txt", context)

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[owner_email],
        )
        email.attach_alternative(html_content, "text/html")

        try:
            email.send()
            return True
        except Exception as e:
            print(f"Response notification failed: {e}")
            return False
