from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from movies.models import *
from django.http import JsonResponse

def signup(request):
    if request.user.is_authenticated:
        return redirect('movies:index')
    if request.method =='POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('movies:index')
    else:
        form = UserCreationForm()

    context={
        'form' : form
    }
    return render(request, 'accounts/signup.html', context)

def login(request):

    if request.method=='POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return  redirect('movies:index')

    else:
        form = AuthenticationForm()

    context = {
        'form' : form
    }

    return render(request, 'accounts/login.html', context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('movies:index')

def detail(request, username):
    User = get_user_model()
    user = get_object_or_404(User, username=username)
    genre = Genre.objects.all()
    context = {
        'user': user,
        'genre': genre,
    }
    return render(request, 'accounts/detail.html', context)

@login_required
def follow(request, username):
    #팔로우 대상
    following = get_object_or_404(get_user_model(), username = username)
    #팔로워
    follower = request.user

    if follower != following :
        if following.followers.filter(pk=follower.pk).exists():
            following.followers.remove(follower)
        else:
            following.followers.add(follower)

    return redirect('accounts:detail', following.username)

@login_required
def genlike(request, pk):
    user = request.user
    genre = get_object_or_404(Genre, pk=pk)

    if genre.gen_users.filter(pk=user.pk).exists():
        genre.gen_users.remove(user)
        liked = False
    else:
        genre.gen_users.add(user)
        liked = True
    context = {
        'liked': liked,
    }

    return JsonResponse(context)
