from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from custom_auth_service.auth_db.models import User
from .models import Contact

import io
from django.http import HttpResponseForbidden
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .forms import ContactForm
from django.db.models import Count, Q  # Ajout de Q pour les requêtes complexes


def contact_detail(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    data = {
        'id': contact.id,
        'first_name': contact.first_name,
        'last_name': contact.last_name,
        'phone_number': contact.phone_number,
        'email': contact.email
    }
    return JsonResponse(data)

def add_contact(request):
    user_account = request.user.contact  # Remplacer 'profile' par 'account'
    form = ContactForm(request.POST or None)
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.account = request.user.account  # Remplacer 'profile' par 'account'
            contact.save()
            messages.success(request, 'Contact has been added successfully.')
            return redirect('home')
        else:
            form.add_error(None, 'Fill fields correctly!')
    context = {
        'form': form,
        'account': user_account,  # Remplacer 'profile' par 'account'
    }
    return render(request, 'create_contact.html', context)

def home(request):
    print("fonction home")
    if 'access_token' in request.session:
        print("Bienvenue sur la page d'accueil ")
        user_id = request.session.get('_auth_user_id')
        print("user id",user_id)
        if user_id:
            contacts = Contact.objects.using('annuaire_db').filter(user=user_id)
            context = {'contacts': contacts}
            print("retour",context)
            return render(request, 'index.html', context)
        else:
            return HttpResponse("Erreur d'authentification")
    else:
        print("pas authentifié depuis la fonction home ")
        # Gérez le cas où l'utilisateur n'est pas connecté
        return redirect('auth_login')
   
def retrograde_contact(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.user.status == User.Status.superadmin:
        # Vous pouvez personnaliser cette condition en fonction de vos besoins
        if user.status == User.Status.admin:
            user.status = User.Status.utilisateur
            user.save()
            messages.success(request, f'User {user.username} retrograded to Utilisateur.')
        else:
            messages.warning(request, 'You can only retrograde Admin users.')

        return redirect('home')
    else:
        messages.warning(request, 'You are not authorized to perform this action.')
        return HttpResponseForbidden()

def promove_contact(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.user.status == User.Status.superadmin:
        # Vous pouvez personnaliser cette condition en fonction de vos besoins
        if user.status == User.Status.utilisateur:
            user.status = User.Status.admin
            user.save()
            messages.success(request, f'User {user.username} promoted to Admin.')
        else:
            messages.warning(request, 'You can only promote Utilisateur users.')

        return redirect('home')
    else:
        messages.warning(request, 'You are not authorized to perform this action.')
        return HttpResponseForbidden()

def contact(request):
    contacts = Contact.objects.all()

    context = {'contacts': contacts}
    return render(request, 'contact_list.html', context)

def search_contact(request):
    search_query = request.GET.get('q', '')
    user = request.user.contact

    contacts = Contact.objects.filter(contact=user)

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

    return JsonResponse({'contacts': serialized_contacts})

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