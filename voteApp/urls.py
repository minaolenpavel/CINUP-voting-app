from django.urls import path, include
from . import views

app_name = "voteApp"
urlpatterns = [
    path('', views.login, 
        name='login'),
    path('index/', views.index, 
        name="index"),
    path('details/<uuid:question_id>/', views.details, 
        name='details'),
    path('vote/<uuid:question_id>/', views.vote, 
        name="vote"),
    path('results/', views.results, 
        name='results'),
    path('question_results/<int:question_id>/', views.question_results, 
        name='question_results'),
]
