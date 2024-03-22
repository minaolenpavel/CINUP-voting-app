from django.urls import path, include
from . import views

app_name = "Vote app"
urlpatterns = [
    path("", views.index, 
         name="index"),
    path("login/", views.login, 
         name="login"),
]
