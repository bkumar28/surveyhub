from django.db import migrations


def populate_default_categories(apps, schema_editor):
    TemplateCategory = apps.get_model("yourappname", "TemplateCategory")
    default_categories = [
        ("FEEDBACK", "Customer Feedback"),
        ("RESEARCH", "Market Research"),
        ("HR", "Human Resources"),
        ("EDUCATION", "Education"),
        ("HEALTHCARE", "Healthcare"),
        ("EVENT", "Event Feedback"),
        ("PRODUCT", "Product Evaluation"),
        ("GENERAL", "General Purpose"),
    ]

    for i, (key, label) in enumerate(default_categories):
        TemplateCategory.objects.get_or_create(
            name=key, defaults={"description": label, "order": i}
        )


class Migration(migrations.Migration):
    dependencies = [
        ("yourappname", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(populate_default_categories),
    ]
