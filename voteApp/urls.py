from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from.views import GenerateProxyVoteView, UseProxyVoteView



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
    path('', LogoutView.as_view(next_page='voteApp:login/'), 
        name='logout'),
    path('generate-proxy-vote/', GenerateProxyVoteView.as_view(), 
        name='generate_proxy_vote'),
    path('use-proxy-vote/', UseProxyVoteView.as_view(), 
        name='use_proxy_vote'),
]
