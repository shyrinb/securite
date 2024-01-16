from securite_projet import settings
from .models import User
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from .forms import UserRegistrationForm, LoginForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login,get_user_model
from .backends import UtilisateurAPIBackend
from django.contrib.auth import authenticate, login
from django.db.models import Count
from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics
import logging

logger = logging.getLogger(__name__)

def signup(request):
    form = UserRegistrationForm(request.POST or None)
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print("form est valide ")
            form.save()
            print("inscription effectuée")
        else:
            messages.error(request, 'Fill the form correctly!')

    return render(request, 'register.html', {'form': form})

def user_login(request):
    form = LoginForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        user = form.save(request)
        
        if user is not None:
            print("Correct username and password")
            print(f'User authenticated: {user.username}')
            next_url = request.GET.get('next', reverse('annuaire_home'))
            print(f"Redirection vers {next_url}")
            return redirect(next_url)

    return render(request, 'login.html', context={'form': form})


def user_logout(request):
    if 'access_token' in request.session:
        del request.session['access_token']
        messages.success(request, 'You have been successfully logged out.')
    return redirect('auth_login')
    

def userprofile(request):
    account = request.user
    return render(request, 'userprofile.html', {'account': account})

def change_password(request):
    account = request.user
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Fill the form correctly!')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'update_password.html', {'form': form, 'title': 'Change Password', 'account': account})

def desinscrire(request):
    return render(request, 'signup.html')

def update_profile(request):
    account = request.user.account
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        account_form = UserEditForm(
            instance=request.user, data=request.POST)
        if user_form.is_valid() and account_form.is_valid():
            user_form.save()
            account_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserEditForm(instance=request.user)
        account_form = AccountEditForm(instance=request.user.account)
    return render(request, 'profileUpdate.html', {'user_form': user_form, 'account_form': account_form, 'account': account})
