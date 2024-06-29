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
    path('results/', views.results, 
        name='results'),
    path('question_results/<int:question_id>/', views.question_results, 
        name='question_results'),
    path('generate-keys/', views.generate_proxy_keys, 
        name='generate_proxy_keys'),
    path('use-proxy-key/', views.use_proxy_key, 
        name='use_proxy_key'),
    path('gen-success/', views.gen_success,
        name="gen_success"),
    path('', LogoutView.as_view(next_page='voteApp:login/'), 
        name='logout'),
    
]
