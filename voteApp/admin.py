# Import the admin module from Django's contrib package
from django.contrib import admin
# Import the models from the current directory (app)
from .models import Question, Choice

# Customize the header of the admin site
admin.site.site_header = "Assemblée générale"
# Customize the title of the admin site
admin.site.site_title = "Admin area"
# Customize the index title of the admin site
admin.site.index_title = "Welcome to voting admin area"

# Define an inline admin class for the Choice model
# This allows you to edit Choice instances directly from the Question admin page
class ChoiceInLine(admin.TabularInline):
    model = Choice  # The model to be edited inline
    extra =  3  # The number of extra forms to display

# Define an admin class for the Question model
# This class specifies how the Question model should be displayed in the admin site
class QuestionAdmin(admin.ModelAdmin):
    # Define the fieldsets for the Question model
    # Fieldsets are sections of the form, divided by fieldsets, which can be collapsed
    fieldsets = [
        (None, {'fields':['question_text']}),  # A fieldset with no title, containing the 'question_text' field
        ('Date Information', {'fields': ['pub_date'], 'classes': ['collapse']}),  # A fieldset titled 'Date Information', containing the 'pub_date' field, which is collapsible
    ]
    # Include the ChoiceInLine admin class in the admin interface for the Question model
    inlines = [ChoiceInLine]

# Register the Question model with the admin site and specify the QuestionAdmin class to use for its admin interface
admin.site.register(Question, QuestionAdmin)
