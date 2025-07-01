import csv

from django.conf import settings
from django.http import HttpResponse


def export_survey_responses_csv(survey):
    """Export survey responses to CSV format"""
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f'attachment; filename="{survey.title}_responses.csv"'
    )

    writer = csv.writer(response)

    # Header row
    headers = ["Response ID", "Submitted At", "User", "Is Complete"]
    for question in survey.questions.all():
        headers.append(question.title)
    writer.writerow(headers)

    # Data rows
    for survey_response in survey.responses.all():
        row = [
            survey_response.id,
            survey_response.submitted_at,
            survey_response.user.username if survey_response.user else "Anonymous",
            survey_response.is_complete,
        ]

        # Add answers
        for question in survey.questions.all():
            try:
                answer = survey_response.answers.get(question=question)
                if question.field_type == "T":
                    row.append(answer.text_answer)
                elif question.field_type == "N":
                    row.append(answer.number_answer)
                elif question.field_type == "B":
                    row.append(answer.boolean_answer)
                elif question.field_type in ["SC", "MC"]:
                    row.append(", ".join(answer.choice_answers))
                else:
                    row.append(answer.text_answer)
            except Exception:
                row.append("")

        writer.writerow(row)

    return response


def generate_survey_qr_code(survey):
    """Generate QR code for survey"""
    from io import BytesIO

    import qrcode

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    survey_url = f"{settings.FRONTEND_URL}/survey/{survey.id}"
    qr.add_data(survey_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer


def validate_survey_logic(survey):
    """Validate survey conditional logic"""
    errors = []

    for question in survey.questions.all():
        if question.depends_on:
            # Check if the dependent question exists and comes before this question
            if question.depends_on.order >= question.order:
                errors.append(
                    f"Question '{question.title}' depends on a question that "
                    + "comes after it"
                )

            # Check if condition value is valid for the dependent question type
            if question.depends_on.field_type in ["SC", "MC"]:
                if question.condition_value not in question.depends_on.options:
                    errors.append(
                        f"Invalid condition value for question '{question.title}'"
                    )

    return errors
