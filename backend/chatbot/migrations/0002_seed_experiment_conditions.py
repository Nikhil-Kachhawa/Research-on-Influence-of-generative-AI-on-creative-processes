from django.db import migrations


def create_conditions(apps, schema_editor):
    ExperimentCondition = apps.get_model(
        "chatbot",
        "ExperimentCondition"
    )

    ExperimentCondition.objects.get_or_create(
        name="idea-generator"
    )

    ExperimentCondition.objects.get_or_create(
        name="critical-evaluator"
    )


def remove_conditions(apps, schema_editor):
    ExperimentCondition = apps.get_model(
        "chatbot",
        "ExperimentCondition"
    )

    ExperimentCondition.objects.filter(
        name__in=[
            "idea-generator",
            "critical-evaluator",
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("chatbot", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            create_conditions,
            remove_conditions,
        ),
    ]