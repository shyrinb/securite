from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from custom_auth_service.auth_db.forms import AddContactForm
from custom_auth_service.auth_db.models import User
from custom_auth_service.auth_db.views import status_user
from .models import Contact

import io
from django.http import HttpResponseForbidden
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .forms import ContactForm
from django.db.models import Count, Q  # Ajout de Q pour les requêtes complexes


def add_contact(request):
   if 'access_token' in request.session:
        form = AddContactForm(request.POST or None)
    
        if request.method == 'POST':
            form = AddContactForm(request.POST)
            if form.is_valid():
                print("form est valide ")
                form.save()
                print("inscription effectuée")
        else:
            messages.error(request, 'Fill the form correctly!')
       
        return render(request, 'create_contact.html', {'form': form})

def home(request):
    print("fonction home")
    if 'access_token' in request.session:
        print("Bienvenue sur la page d'accueil ")
        user_id = request.session.get('user_id')
        print("user id",user_id)
        user_status_data = status_user(request) 
        if user_id:
            contacts = Contact.objects.using('annuaire_db').filter(user_id=user_id)
            context = {'contacts': contacts, 'user_status': user_status_data}
            print("retour",context)
            return render(request, 'index.html', context)
        else:
            return HttpResponse("Erreur d'authentification")
    else:
        print("pas authentifié depuis la fonction home ")
        # Gérez le cas où l'utilisateur n'est pas connecté
        return redirect('auth_login')
   
def go_to_retrograde(request,contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    user=User.objects.using('auth_db').filter(contact_relation=contact.id).first()
    data={
        'last_name':contact.last_name,
        'first_name':contact.first_name,
        'contact_id':contact.id,
        'user_id':user.id
    }
    return render(request, 'retrograde.html',{'result':data})
    
def retrograde_contact(request, contact_id):
    if 'access_token' in request.session:
        user_id = request.session.get('user_id')
        user_admin =User.objects.using('auth_db').get(id=user_id)
        contact = get_object_or_404(Contact, id=contact_id)
        user=User.objects.using('auth_db').filter(contact_relation=contact.id).first()
        print("User ID:{user.id} ")

        if user_admin.status == 2 or user_admin.status == 1:
            print("la personne est un admin")
                # Vous pouvez personnaliser cette condition en fonction de vos besoins
            if user.status == 1: # RETROGRADE ADMIN VERS UTILISATEUR
                if request.method == 'POST':
                    print("l'utilisateur est un admin ")
                    user.status = 0
                    user.save()
                    messages.success(request, f'User {user.username} promoted to Admin.')
                else:
                    messages.warning(request, 'You can only promote Utilisateur users.')
                    return redirect(reverse('annuaire_user:home'))    
        else:
            messages.warning(request, 'You are not authorized to perform this action.')
            return HttpResponseForbidden()
    
def go_to_promove(request,contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    user=User.objects.using('auth_db').filter(contact_relation=contact.id).first()
    data={
        'last_name':contact.last_name,
        'first_name':contact.first_name,
        'contact_id':contact.id,
        'user_id':user.id
    }
    return render(request, 'promouvoir.html',{'result':data})
    
def promove_contact(request, contact_id):
    if 'access_token' in request.session:
        user_id = request.session.get('user_id')
        user_admin =User.objects.using('auth_db').get(id=user_id)
        contact = get_object_or_404(Contact, id=contact_id)
        user=User.objects.using('auth_db').filter(contact_relation=contact.id).first()
        print("User ID:{user.id} ")

        if request.method == 'POST':
            if user_admin.status == 2 or user_admin.status == 1:
                # Vous pouvez personnaliser cette condition en fonction de vos besoins
                if user.status == 0: # PROMOTION UTILISATEUR EN ADMIN
                    user.status = 1
                    user.save()
                    messages.success(request, f'User {user.username} promoted to Admin.')
                else:
                    messages.warning(request, 'You can only promote Utilisateur users.')

                return redirect(reverse('annuaire_user:home'))
            else:
                messages.warning(request, 'You are not authorized to perform this action.')
                return HttpResponseForbidden()

def contact(request):
    contacts = Contact.objects.all()
    if 'access_token' in request.session:
       # user_id = request.session.get('user_id')
        user_status_data = status_user(request)  # Appelez la fonction status_user avec l'objet request

        context = {'contacts': contacts, 'user_status': user_status_data}
        print("context de contact list", context)
        return render(request, 'contact-list.html', context)
    else:
        # Gérez le cas où l'utilisateur n'est pas connecté
        return render(request, 'contact-list.html', {'contacts': contacts, 'user_status': None})

def go_to_search(request):
    return render(request, 'search.html')
    
def search_contact(request):
    if 'access_token' in request.session:
        search_query = request.GET.get('query', '')
        user_id = request.session.get('user_id')
        contacts = Contact.objects.filter(user_id=user_id)

        if search_query:
            contacts = contacts.filter(
                first_name__startswith=search_query) | contacts.filter(
                last_name__startswith=search_query) | contacts.filter(
                phone_number__startswith=search_query) | contacts.filter(
                email__startswith=search_query)

        serialized_contacts = []
        for contact in contacts:
            serialized_contacts.append({
                'id': contact.id,
                'first_name': contact.first_name,
                'last_name': contact.last_name,
                'phone_number': contact.phone_number,
                'email': contact.email
            })
        print("reponse:",serialized_contacts)
        return render(request, 'search.html',{'contacts': serialized_contacts})

def update_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    account = request.user.account

    if contact.account != request.user.account:
        messages.warning(request, 'You are not authorized to do this.')
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ContactForm(instance=contact)

    return render(request, 'update.html', {'form': form, 'title': 'Update Contact', 'account': account})

def delete_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    account = request.user.account

    if contact.account != request.user.account:
        messages.warning(request, 'You are not authorized to do this.')
        return HttpResponseForbidden()

    if request.method == 'POST':
        contact.delete()
        messages.success(request, 'Contact deleted successfully.')
        return redirect('home')

    return render(request, 'delete_contact.html', {'contact': contact, 'account': account})