from django.db import migrations, models
from django.utils import timezone
from datetime import timedelta

def set_default_question_expiration(apps, schema_editor):
    Question = apps.get_model('voteApp', 'Question')
    for question in Question.objects.all():
        question.question_expiration = question.question_date + timedelta(hours=3)  # Adjust based on your default logic
        question.save()

class Migration(migrations.Migration):

    dependencies = [
        ('voteApp', '0015_remove_question_question_expiration'),
    ]

    operations = [
        migrations.RunPython(set_default_question_expiration),
    ]
