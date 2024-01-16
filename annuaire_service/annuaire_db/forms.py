from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=10, required=False)  
    email = forms.CharField(max_length=100, required=True) 
    first_name = forms.CharField(max_length=50, required=True) 
    last_name = forms.CharField(max_length=50, required=True) 

    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'phone_number', 'email']

    def save(self, commit=True):
        self.full_clean()
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        email = cleaned_data.get('email')
        telephone = cleaned_data.get('phone_number')

        if commit:
            # Créer le contact sans spécifier l'utilisateur
            contact, created = Contact.objects.using('annuaire_db').get_or_create()

            # Mettre à jour les champs du contact
            contact.last_name = last_name
            contact.email = email
            contact.phone_number = telephone
            contact.first_name = first_name

            # Si la requête contient un utilisateur, l'associer au contact
            if hasattr(self, 'request') and hasattr(self.request, 'user'):
                contact.user = self.request.user

            # Sauvegarder le contact dans la base de données annuaire_db
            contact.save(using='annuaire_db')

        return contact