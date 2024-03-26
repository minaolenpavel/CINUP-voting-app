from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.urls import reverse
from .models import Question, Choice
from django.contrib.auth import authenticate, login as auth_login
# Create your views here.

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

def details(request, question_id):
    print(f"Received question_id: {question_id}")
    question = get_object_or_404(Question, question_id=question_id)
    print(f"Retrieved question: {question}")
    return render(request, 'details.html', {'question' : question})