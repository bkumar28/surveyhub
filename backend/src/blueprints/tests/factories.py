import factory
from blueprints.models import BlueprintCategory, QuestionBlueprint, SurveyBlueprint
from core.factories import UserFactory


class BlueprintCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BlueprintCategory

    name = factory.Sequence(lambda n: f"Category {n}")
    description = factory.Faker("sentence")
    order = factory.Sequence(int)


class SurveyBlueprintFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SurveyBlueprint

    name = factory.Sequence(lambda n: f"Survey {n}")
    description = factory.Faker("sentence")
    category = factory.SubFactory(BlueprintCategoryFactory)
    tags = factory.LazyFunction(lambda: ["tag1", "tag2"])
    is_public = True
    created_by = factory.SubFactory(UserFactory)
    blueprint_data = factory.LazyFunction(lambda: {"title": "Survey", "questions": []})


class QuestionBlueprintFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = QuestionBlueprint

    title = factory.Sequence(lambda n: f"Question {n}")
    field_type = "R"
    category = "general"
    blueprint_data = factory.LazyFunction(
        lambda: {"field_type": "R", "scale_min": 1, "scale_max": 5}
    )
