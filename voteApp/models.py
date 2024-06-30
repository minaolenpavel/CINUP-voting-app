# Import the models module from Django's db package
from django.db import models
from django.contrib.auth.models import User, AbstractUser
import uuid
from django.conf import settings
import datetime
from django.utils import timezone

# Define a model class for Question
class Question(models.Model):
    # Define a CharField with a maximum length of  300 characters
    question_text = models.CharField(max_length=300)
    # Define a DateTimeField to store the date the question was published
    question_date = models.DateTimeField('date de publication')
    question_desc = models.TextField(blank=True)
    question_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    voters = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='voted_questions', blank=True)    # Define the string representation of the model instance
    def __str__(self):
        # Return the text of the question as the string representation
        return self.question_text

# Define a model class for Choice
class Choice(models.Model):
    # Define a ForeignKey field to link each choice to a question
    # The 'on_delete=models.CASCADE' argument means that when the referenced question is deleted, also delete the choices associated with it
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # Define a CharField with a maximum length of  200 characters for the choice text
    choice_text = models.CharField(max_length=200)
    # Define an IntegerField to store the number of votes for the choice, with a default value of  0
    votes = models.IntegerField(default=0)
    voters = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='votes', blank=True)

    # Define the string representation of the model instance
    def __str__(self) -> str:
        # Return the text of the choice as the string representation
        return self.choice_text

class CustomUser(AbstractUser):
    display_name = models.CharField(max_length=255, default='')

class UserKey(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    access_key = models.CharField(max_length=20, blank=True, editable=False)
    key_generation_date = models.DateTimeField(default=timezone.now)
    activation_date = models.DateTimeField(null=True, blank=True)
    key_expiration_date = models.DateTimeField(null=True, blank=True)
    
    @property
    def is_valid(self):
        return self.key_expiration_date is None or self.key_expiration_date > timezone.now()

    def save(self, *args, **kwargs):
        if self.activation_date:
            self.key_expiration_date = self.activation_date + datetime.timedelta(hours=24)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.access_key} ({'Valid' if self.is_valid else 'Invalid'})"