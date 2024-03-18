# Import the models module from Django's db package
from django.db import models

# Define a model class for Question
class Question(models.Model):
    # Define a CharField with a maximum length of  300 characters
    question_text = models.CharField(max_length=300)
    # Define a DateTimeField to store the date the question was published
    question_date = models.DateTimeField('date published')
    question_desc = models.CharField(max_length=500)

    # Define the string representation of the model instance
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

    # Define the string representation of the model instance
    def __str__(self) -> str:
        # Return the text of the choice as the string representation
        return self.choice_text
