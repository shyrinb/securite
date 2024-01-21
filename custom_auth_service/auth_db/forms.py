from django import forms
from django.contrib.auth import authenticate, login
from annuaire_service.annuaire_db.models import Contact
from annuaire_service.annuaire_db.forms import ContactForm
from .backends import UtilisateurAPIBackend
from .models import User, Historique
from django.contrib.auth import login
from django.utils import timezone


class UserRegistrationForm(forms.ModelForm): 
    username=forms.CharField(max_length=100, required=True) 
    email = forms.CharField(max_length=100, required=True) 
    first_name = forms.CharField(max_length=50, required=True) 
    last_name = forms.CharField(max_length=50, required=True) 
    phone_number = forms.CharField(max_length=10, required=False) 
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(
        label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                self.add_error('confirm_password', 'Passwords do not match.')

        if len(password) < 4:
            self.add_error(
                'password', 'Password should be at least 4 characters long.')

    def save(self, commit=True):
        cleaned_data = super().clean()
        user = super().save(commit=False)

        user.email = cleaned_data['email']
        user.first_name = cleaned_data['first_name']
        user.last_name = cleaned_data['last_name']
        user.phone_number = cleaned_data.get('phone_number', '')
        user.set_password(cleaned_data['password'])
        print("mot de passe hashé")

        if commit:
            user.save(using='auth_db')  # Enregistrez l'utilisateur
            print("Utilisateur enregistré")

            contact_form = ContactForm(self.cleaned_data)
            print("contact form", contact_form)
            if contact_form.is_valid():
                contact = contact_form.save(commit=True)
                if contact:
                    print("contact", contact)
                    contact = Contact.objects.create(
                        first_name=self.cleaned_data['first_name'],
                        last_name=self.cleaned_data['last_name'],
                        phone_number=self.cleaned_data.get('phone_number', ''),
                        email=self.cleaned_data['email'],
                        user_id=user.id
                    )
                    contact.save(using='annuaire_db')
                    print("Contact enregistré")

                    # Associez le contact à l'utilisateur, mais ne l'enregistrez pas encore dans la base de données auth_db
                    user.contact_relation = contact

                    # Maintenant, sauvegardez l'utilisateur avec le contact associé
                    user.save(using='auth_db')
                    print("lien ajouté")

                    # Créez ou récupérez l'objet Historique associé à l'utilisateur
                    historique = Historique.objects.using('auth_db').create(
                        user=user,
                        action="creation",
                        timestamp=timezone.now()
                    )
                    print("historique enregistre")
                    historique.save(using='auth_db')
                else:
                    print("Erreur de validation dans le modèle Contact:", contact_form.errors)
            else:
                print("Erreur de validation dans le formulaire Contact:", contact_form.errors)
        return user

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

    def save(self, request):
        cleaned_data = self.cleaned_data
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            backend = UtilisateurAPIBackend()
            user = backend.authenticate(username=username, request=request,password=password)

            if user:
                user.backend = 'custom_auth_service.auth_db.backends.UtilisateurAPIBackend'
                login(request, user)
                print("User logged in successfully.")
                # Créez ou récupérez l'objet Historique associé à l'utilisateur
                historique = Historique.objects.using('auth_db').create(
                    user=user,
                    action="connexion",
                    timestamp=timezone.now()
                )
                print("historique enregistre")
                historique.save(using='auth_db')
                print("user",user)
                return user
            
        print('Échec de l\'authentification.')
        return('Invalid username or password. Please try again.')

class UserContactEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    # Additional fields from Contact model
    phone_number = forms.CharField(max_length=10, required=False)

    def save(self, commit=True):
        user = super().save(commit=False)
        historique = Historique.objects.using('auth_db').create(
            user=user,
            action="mise_a_jour",
            commentaire="contact",
            timestamp=timezone.now()
        )
        
        print("historique mis à jour")
        historique.save(using='auth_db')
        if commit:
                user.save()
        # Update associated Contact
        contact = user.contact.first()
        contact.first_name = user.first_name
        contact.last_name = user.last_name
        contact.email = user.email
        contact.phone_number = self.cleaned_data['phone_number']
        contact.save()

        print("contact mis à jour")

        if commit:
            user.save(using='auth_db')
            print("user mise à jour")

        return user
    
class AddContactForm(forms.ModelForm): 
    username=forms.CharField(max_length=100, required=True) 
    email = forms.CharField(max_length=100, required=True) 
    first_name = forms.CharField(max_length=50, required=True) 
    last_name = forms.CharField(max_length=50, required=True) 
    phone_number = forms.CharField(max_length=10, required=False) 
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(
        label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                self.add_error('confirm_password', 'Passwords do not match.')

        if len(password) < 4:
            self.add_error(
                'password', 'Password should be at least 4 characters long.')

    def save(self, commit=True):
        cleaned_data = super().clean()
        user = super().save(commit=False)

        user.email = cleaned_data['email']
        user.first_name = cleaned_data['first_name']
        user.last_name = cleaned_data['last_name']
        user.phone_number = cleaned_data.get('phone_number', '')
        user.set_password(cleaned_data['password'])
        print("mot de passe hashé")

        if commit:
            user.save(using='auth_db')  # Enregistrez l'utilisateur
            print("Utilisateur enregistré")

            contact_form = ContactForm(self.cleaned_data)
            print("contact form", contact_form)
            if contact_form.is_valid():
                contact = contact_form.save(commit=True)
                if contact:
                    print("contact", contact)
                    contact = Contact.objects.create(
                        first_name=self.cleaned_data['first_name'],
                        last_name=self.cleaned_data['last_name'],
                        phone_number=self.cleaned_data.get('phone_number', ''),
                        email=self.cleaned_data['email'],
                        user_id=user.id
                    )
                    contact.save(using='annuaire_db')

                    print("Contact enregistré")
                    # Associez le contact à l'utilisateur, mais ne l'enregistrez pas encore dans la base de données auth_db
                    user.contact_relation = contact

                    # Maintenant, sauvegardez l'utilisateur avec le contact associé
                    user.save(using='auth_db')
                    print("lien ajouté")

                    # Créez ou récupérez l'objet Historique associé à l'utilisateur
                    historique = Historique.objects.using('auth_db').create(
                        user=user,
                        action="creation",
                        commentaire="nouveau contact par admin",
                        timestamp=timezone.now()
                    )
                    print("historique enregistre")
                    historique.save(using='auth_db')
                else:
                    print("Erreur de validation dans le modèle Contact:", contact_form.errors)
            else:
                print("Erreur de validation dans le formulaire Contact:", contact_form.errors)
        return user