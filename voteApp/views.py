from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Choice, Question, ProxyVote
from django.contrib.auth.models import Group
from django.urls import reverse
from django.conf import settings
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

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Choice

@login_required
def vote(request, question_id):
    if request.method == 'POST':
        choice_id = request.POST.get('choice_id')
        choice = get_object_or_404(Choice, id=choice_id)
        # Check if the user is part of the "presidence" group
        if request.user.groups.filter(name="presidence").exists():
            # If the user is part of the "presidence" group, do not count the vote
            messages.error(request, 'Vous n\'avez pas le droit de voter.', extra_tags="no_right_to_vote")
            return render(request, 'details.html', {'question': choice.question})
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
    presidence_group = Group.objects.filter(name="presidence").first()
    
    # Filter out superusers and users who are part of the "presidence" group
    if presidence_group:
        all_users = User.objects.exclude(is_superuser=True).exclude(groups__in=[presidence_group])
    else:
        all_users = User.objects.exclude(is_superuser=True)
        # Prepare a dictionary to store whether each user has voted for any choice in this question
    user_votes = {user: user in users_who_voted for user in all_users}
    return render(request, 'question_results.html', {'question': question, 'choices': choices, 'user_votes': user_votes})


@login_required
def generate_proxy_keys(request):
    if request.method == 'POST':
        # Create a new ProxyVote instance for the current user
        proxy_vote = ProxyVote.objects.create(user=request.user, generated_by=request.user)
        
        # Redirect to success page with the key as a query parameter
        return redirect(f"{reverse('voteApp:gen_success')}?generated_key={proxy_vote.key}")
    else:
        # Render the template to generate proxy keys
        return render(request, 'generate_proxy_keys.html')

@login_required
def gen_success(request):
    generated_key = request.GET.get('generated_key', '')
    return render(request, 'gen_proxy_success.html', {'generated_key': generated_key})

@login_required
def use_proxy_key(request):
    if request.method == 'POST':
        key = request.POST.get('proxy_key')
        if not key:
            messages.error(request, 'Please enter a proxy key.')
            return redirect('voteApp:use_proxy_key')
        try:
            proxy_vote = ProxyVote.objects.get(key=key)
            if proxy_vote.used:
                messages.error(request, 'This key has already been used.')
                return redirect('voteApp:use_proxy_key')
            # Mark the proxy key as used
            proxy_vote.used = True
            proxy_vote.save()
            # Logic to mark the original user as having voted goes here
            messages.success(request, 'Proxy key successfully used.')
            return redirect('voteApp:success_page')  # Replace with your actual success page URL
        except ProxyVote.DoesNotExist:
            messages.error(request, 'Proxy key not found.')
            return redirect('voteApp:use_proxy_key')
    return render(request, 'use_proxy_key.html')

@login_required
def view_generated_proxy_keys(request):
    # Fetch all proxy keys generated by the current user
    user_proxy_keys = ProxyVote.objects.filter(user=request.user)
    context = {
        'proxy_keys': user_proxy_keys
    }
    return render(request, 'view_generated_proxy_keys.html', context)

@login_required
def view_used_proxy_keys(request, user_id):
    User = get_user_model()
    user = User.objects.get(id=user_id)
    proxy_keys = ProxyVote.objects.filter(user=user, used=True)
    return render(request, 'view_used_proxy_keys.html', {'proxy_keys': proxy_keys})