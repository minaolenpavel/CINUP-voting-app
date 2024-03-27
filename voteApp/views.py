from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.urls import reverse
from .models import Question, Choice
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def index(request):
    questionsList = Question.objects.order_by('-question_date')[:5] 
    print(questionsList)
    #this last part is about the number of questions to be displayed by pub_date, here it will display the last 5 questions
    context = {"questionsList" : questionsList }
    return render(request, "index.html", context)


    
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect(reverse('voteApp:index'))
        else :
            return render(request, "login.html", {'error': "Nom d'utilisateur ou mot de passe erronés"})
    else: 
        return render(request, "login.html")

@login_required
def details(request, question_id):
    question = get_object_or_404(Question.objects.prefetch_related('choice_set'), question_id=question_id)
    return render(request, 'details.html', {'question' : question})