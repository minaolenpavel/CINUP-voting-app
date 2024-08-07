from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseForbidden
from.forms import AccessKeyForm
from .models import Choice, Question, CustomUser, UserKey
from .forms import *
import secrets
import string
from django.utils import timezone
from datetime import timedelta

@login_required
def index(request):
    questionsList = Question.objects.order_by('-question_date')
    return render(request, "index.html", {"questionsList" : questionsList, "now" : timezone.now })

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
    print(question.question_expiration)
    return render(request, 'details.html', {'question' : question, "now" : timezone.now()})



@login_required
def vote(request, question_id):
    if request.method == 'POST':
        choice_id = request.POST.get('choice_id')
        choice = get_object_or_404(Choice, id=choice_id)  
        question = choice.question
        if question.question_expiration <= timezone.now():
            messages.error(request, 'Cette question n\'est plus d\'actualité.', extra_tags="not_allowed")
            return render(request, 'details.html', {'question': choice.question})
        if request.user.is_superuser or request.user.is_staff:
            messages.error(request, 'Vous n\'êtes pas autorisé à voter.', extra_tags="not_allowed")
            return render(request, 'details.html', {'question': choice.question})
        if request.user in choice.question.voters.all():
            messages.error(request, 'Vous avez déjà voté !', extra_tags="already_voted")
            return render(request, 'details.html', {'question': choice.question})
        else:
            #only increment the vote count and add the user to the voters if they are not part of the "presidence" group
            choice.votes += 1
            choice.voters.add(request.user) #add the user to the voters
            choice.save()
            choice.question.voters.add(request.user)
            messages.success(request, 'Votre vote a bien été enregistré', extra_tags="vote_recorded")
            return redirect('voteApp:index') #redirect to the index page or wherever you want
    else:
        return redirect('voteApp:index')

@login_required
def question_results(request, question_id):
    User = get_user_model()
    question = get_object_or_404(Question, id=question_id)
    choices = Choice.objects.filter(question=question).prefetch_related('voters')
    # Get all users who have voted for any choice in this question
    users_who_voted = set()
    for choice in choices:
        users_who_voted.update(choice.voters.all())
    #get all users except superusers
    all_users = User.objects.exclude(is_superuser=True).exclude(is_staff=True)
    #prepare a dictionary to store whether each user has voted for any choice in this question
    user_votes = {user: user in users_who_voted for user in all_users}
    sorted_user_votes = sorted(user_votes.items(), key=lambda item: not item[1])
    print(user_votes)
    print(sorted_user_votes)
    total_votes = len(users_who_voted)
    return render(request, 'question_results.html', {'question': question, 'choices': choices, 'user_votes': sorted_user_votes, 'total' : total_votes})

@login_required
def generate_key(request):
    if request.method == 'POST':
        form = GenerateKeyForm(request.POST)
        if form.is_valid():
            alphabet = string.ascii_letters
            access_key = ''.join(secrets.choice(alphabet) for i in range(12))  # Generates a 12-character long string
            activation_date = form.cleaned_data['activation_date']
            user = request.user

            # Invalidate previous keys
            UserKey.objects.filter(user=user).update(key_expiration_date=timezone.now())

            # Create new key
            new_key = UserKey.objects.create(
                user=user,
                access_key=access_key,
                activation_date=activation_date,
                key_generation_date=timezone.now()
            )
            return render(request, 'key_generated.html', {'access_key': access_key, 'expiration_date' : new_key.key_expiration_date})
    else:
        form = GenerateKeyForm()
    return render(request, 'generate_key.html', {'form': form})

def access_with_key(request):
    if request.method == 'POST':
        form = AccessKeyForm(request.POST)
        if form.is_valid():
            access_key = form.cleaned_data['access_key']
            try:
                user_key = UserKey.objects.get(access_key=access_key)
                user = user_key.user
                # Check if the key is activated and not expired
                if user_key.activation_date and timezone.now() >= user_key.activation_date and timezone.now() < user_key.activation_date + timedelta(hours=24):
                    # Log the user in
                    user.backend = 'django.contrib.auth.backends.ModelBackend'  # Specify the backend
                    auth_login(request, user)
                    return redirect('voteApp:index')  # Redirect to a target view after successful login
                else:
                    return HttpResponseForbidden('<h1>Invalid or expired key</h1>')
            except UserKey.DoesNotExist:
                return HttpResponseForbidden('<h1>Invalid key</h1>')
    else:
        form = AccessKeyForm()
    return render(request, 'access_with_key.html', {'form': form})
    
@login_required
def key_list(request):
    keys = UserKey.objects.filter(user=request.user).order_by('-key_generation_date')
    return render(request, 'key_list.html', {'keys': keys})

def help_page(request):
    return render(request, 'help.html')