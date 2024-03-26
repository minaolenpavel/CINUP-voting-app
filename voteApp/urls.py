from django.urls import path, include
from . import views

app_name = "voteApp"
urlpatterns = [
     path('', views.login, 
         name='login'),
     path('index/', views.index, 
         name="index"),
     path('details/<uuid:question_id>/', views.details, name='details')
]
