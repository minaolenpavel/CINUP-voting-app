from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.urls import reverse
from .models import Question, Choice
from django.contrib.auth import authenticate
# Create your views here.

def index(request):
    return render(request, "index.html")


    
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else :
            return render(request, "login.html", {'error': "Nom d'utilisateur ou mot de passe erronés"})
    else: 
        return render(request, "login.html")