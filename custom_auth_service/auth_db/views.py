from http.client import HTTPResponse
from django.http import HttpResponseNotFound
from django.utils import timezone
from annuaire_service.annuaire_db.models import Contact
from securite_projet import settings
from .models import Historique, User
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, update_session_auth_hash
from django.contrib import messages
from .forms import UserContactEditForm, UserRegistrationForm, LoginForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login,get_user_model
from django.db.models import Count
from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics
import logging
from django.contrib.auth import get_user_model


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
    

def contact_detail(request, contact_id):
    if 'access_token' in request.session:
        contact = get_object_or_404(Contact, id=contact_id)
        data = {
            'id': contact.id,
            'first_name': contact.first_name,
            'last_name': contact.last_name,
            'phone_number': contact.phone_number,
            'email': contact.email,
            "id_user":contact.user_id
        }
        print(data)
        return render(request, 'contact.html',{'data': data})

def status_user(request):
    if 'access_token' in request.session:
        user_id = request.session.get('user_id')
        user = get_object_or_404(User, id=user_id)
        status_data = {
        'id': user.id,
        'status': user.status
        }
        return status_data

def change_password(request,contact_id):
    if 'access_token' in request.session:
        user_id = request.session.get('user_id')
        # Récupérez l'objet User
        contact = get_object_or_404(Contact, id=contact_id)
        data = {
                'id': contact.id,
                'first_name': contact.first_name,
                'last_name': contact.last_name,
                'phone_number': contact.phone_number,
                'email': contact.email,
                "id_user":contact.user_id
            }
        print(data)
        user = get_object_or_404(User.objects.using("auth_db"), id=data["id_user"])      
        if request.method == 'POST':
            form = PasswordChangeForm(user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                historique = Historique.objects.using('auth_db').create(
                    user=user_id,
                    action="mise_a_jour",
                    commentaire="mot de passe",
                    timestamp=timezone.now()
                )
                
                print("historique mis à jour")
                historique.save(using='auth_db')
                return redirect(reverse('annuaire_user:home'))
            else:
                messages.error(request, 'Fill the form correctly!')
        else:
            form = PasswordChangeForm(request.user)
        return render(request, 'update_password.html', {'form': form, 'title': 'Change Password', 'contact_id': contact_id})

def desinscrire_confirm(request, contact_id):
    if 'access_token' in request.session:
        user_id = request.session.get('user_id')
        print("desinscrire confirm")
        try:
            contact = get_object_or_404(Contact, id=contact_id)
            data = {
                'id': contact.id,
                'first_name': contact.first_name,
                'last_name': contact.last_name,
                'phone_number': contact.phone_number,
                'email': contact.email,
                "id_user":contact.user.id
            }
            print(data)
            user_to_delete = get_object_or_404(User.objects.using("auth_db"), id=data["id_user"])  
            print(f"User to delete : {user_to_delete} with ID : {user_id}") 
        except User.DoesNotExist:
            # Handle the case where the user does not exist
            print(f"User with ID {user_id} does not exist.")
            return HttpResponseNotFound("Utilisateur non trouvé")
        return render(request, 'desinscrire.html', {'user_to_delete': user_to_delete,'contact_id': data["id"]})
    
def desinscrire(request, contact_id):
    if 'access_token' in request.session:
        print("Desinscrire ")

        if request.method == 'POST':
            user_id = request.session.get('user_id')
            contact_to_delete = get_object_or_404(Contact.objects.using("annuaire_db"), id=contact_id)
            print(f"Contact to delete : {contact_to_delete} with ID : {contact_id}") 
            data = {
                'id': contact_to_delete.id,
                'first_name': contact_to_delete.first_name,
                'last_name': contact_to_delete.last_name,
                'phone_number': contact_to_delete.phone_number,
                'email': contact_to_delete.email,
                "id_user": contact_to_delete.user.id
            }
            user_to_delete = get_object_or_404(User.objects.using("auth_db"), id=data["id_user"])  
            print(f"User to delete : {user_to_delete} with ID : {user_id}") 
            contact_to_delete.delete(using='annuaire_db')
            # Supprimez l'utilisateur
            user_to_delete.delete(using='auth_db')
            print("supprimer")
            historique = Historique.objects.using('auth_db').create(
                user=user_id,
                action="suppression",
                commentaire="compte",
                timestamp=timezone.now()
            )
                
            print("historique mis à jour")
            # Déconnectez l'utilisateur
            user_logout(request)
    return HTTPResponse("Une erreur s'est produite. Veuillez réessayer.")


def update_profile(request, contact_id):
    if 'access_token' in request.session:
        print("update profil ")
        contact = get_object_or_404(Contact, id=contact_id)
        data = {
                'id': contact.id,
                'first_name': contact.first_name,
                'last_name': contact.last_name,
                'phone_number': contact.phone_number,
                'email': contact.email,
                "id_user":contact.user_id
        }
        print(data)
        user_id = get_object_or_404(User, id=data["id_user"])
        if request.method == 'POST':
            combined_form = UserContactEditForm(instance=user_id, data=request.POST)
            if combined_form.is_valid():
                combined_form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect(reverse('annuaire_user:home'))
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            combined_form = UserContactEditForm(instance=user_id)

        return render(request, 'profileUpdate.html', {'combined_form': combined_form, 'title': 'Update profil', 'user_id': user_id, 'contact_id':contact_id})