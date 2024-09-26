# Import the admin module from Django's contrib package
from django.contrib import admin
# Import the models from the current directory (app)
from .models import Question, Choice, CustomUser
from django.contrib.auth.admin import UserAdmin

# Customize the header of the admin site
admin.site.site_header = "Assemblée générale du CINUP"
# Customize the title of the admin site
admin.site.site_title = "Zone administrateur"
# Customize the index title of the admin site
admin.site.index_title = "Bienvenue sur la zone admnistrateur"

# Define an inline admin class for the Choice model
# This allows you to edit Choice instances directly from the Question admin page
class ChoiceInLine(admin.TabularInline):
    model = Choice  # The model to be edited inline
    extra =  3  # The number of extra forms to display
    exclude = ('voters',)

# Define an admin class for the Question model
# This class specifies how the Question model should be displayed in the admin site
class QuestionAdmin(admin.ModelAdmin):
    # Define the fieldsets for the Question model
    # Fieldsets are sections of the form, divided by fieldsets, which can be collapsed
    fieldsets = [
        (None, {'fields':['question_text', 'question_desc']}),  # A fieldset with no title, containing the 'question_text' field
        ('Date Information', {'fields': ['question_date', 'question_expiration']}),  # A fieldset titled 'Date Information', containing the 'pub_date' field, which is collapsible
    ]
    # Include the ChoiceInLine admin class in the admin interface for the Question model
    inlines = [ChoiceInLine]
    exclude = ('voters',)

# Register the Question model with the admin site and specify the QuestionAdmin class to use for its admin interface
admin.site.register(Question, QuestionAdmin)

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'display_name', 'is_staff']
    list_filter = ['email', 'display_name', 'is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('display_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                        'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'display_name', 'email', 'password1', 'password2'),
        }),
    )
    search_fields = ['username', 'display_name', 'email']
    ordering = ['username']

# Register the custom user model with the admin site
admin.site.register(CustomUser, CustomUserAdmin)
