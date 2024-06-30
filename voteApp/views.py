from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.urls import reverse
from .models import Choice, Question, ProxyVote  # Ensure ProxyVote is imported correctly
from .forms import GenerateProxyVoteForm  # Ensure forms are imported correctly
from django.views.generic import FormView
from django.views import View
from django.http import HttpResponse
import datetime
# Create your views here.


@login_required
def index(request):
    questionsList = Question.objects.order_by('-question_date')[:10] 
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
            messages.error(request, "Nom d'utilisateur ou mot de passe erroné")
            return render(request, "login.html", {'login_error': "Nom d'utilisateur ou mot de passe erroné"})
    else: 
        return render(request, "login.html")

@login_required
def details(request, question_id):
    question = get_object_or_404(Question.objects.prefetch_related('choice_set'), question_id=question_id)
    return render(request, 'details.html', {'question' : question})



@login_required
def vote(request, question_id):
    if request.method == 'POST':
        choice_id = request.POST.get('choice_id')
        choice = get_object_or_404(Choice, id=choice_id)        
        if request.user in choice.question.voters.all():
            messages.error(request, 'Vous avez déjà voté !', extra_tags="already_voted")
            return render(request, 'details.html', {'question': choice.question})
        else:
            # Only increment the vote count and add the user to the voters if they are not part of the "presidence" group
            choice.votes += 1
            choice.voters.add(request.user) # Add the user to the voters
            choice.save()
            choice.question.voters.add(request.user)
            messages.success(request, 'Votre vote a bien été enregistré', extra_tags="vote_recorded")
            return redirect('voteApp:index') # Redirect to the index page or wherever you want
    else:
        return redirect('voteApp:index') # Redirect to the index page if the request method is not POST

@login_required
def results(request):
    questions = Question.objects.all().prefetch_related('choice_set')
    return render(request, 'results.html', {'questions' : questions})

@login_required
def question_results(request, question_id):
    User = get_user_model()
    question = get_object_or_404(Question, id=question_id)
    choices = Choice.objects.filter(question=question).prefetch_related('voters')
    # Get all users who have voted for any choice in this question
    users_who_voted = set()
    for choice in choices:
        users_who_voted.update(choice.voters.all())
    # Get all users except superusers
    all_users = User.objects.exclude(is_superuser=True)
        # Prepare a dictionary to store whether each user has voted for any choice in this question
    user_votes = {user: user in users_who_voted for user in all_users}
    return render(request, 'question_results.html', {'question': question, 'choices': choices, 'user_votes': user_votes})

class GenerateProxyVoteView(FormView):
    template_name = 'generate_proxy_vote.html'
    form_class = GenerateProxyVoteForm
    success_url = '/success_url/'

    def form_valid(self, form):
        proxy_vote = ProxyVote.objects.create(generated_by=self.request.user, expires_at=form.cleaned_data['expires_at'])
        # You might want to send the key to the user or display it on the page
        return super().form_valid(form)
    
class UseProxyVoteView(View):
    def post(self, request, *args, **kwargs):
        key = request.POST.get('key')
        try:
            proxy_vote = ProxyVote.objects.get(key=key, used_at__isnull=True)
            if proxy_vote.expires_at < datetime.now():
                return HttpResponse("This key has expired.")
            request.user = proxy_vote.generated_by
            proxy_vote.used_by = request.user
            proxy_vote.used_at = datetime.now()
            proxy_vote.save()
            login(request, proxy_vote.generated_by)
            return redirect('voteApp:index')
        except ProxyVote.DoesNotExist:
            return HttpResponse("Invalid key.")