from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView



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
    path('question_results/<int:question_id>/', views.question_results, 
        name='question_results'),
    path('', LogoutView.as_view(next_page='voteApp:login/'), 
        name='logout'),
    path('generate-key/', views.generate_key, 
        name='generate-key'),
    path('access-with-key/', views.access_with_key, 
        name='access-with-key'),
    path('keys/', views.key_list, 
        name='key_list'),
    path('aide/', views.help_page,
        name="aide")
]
