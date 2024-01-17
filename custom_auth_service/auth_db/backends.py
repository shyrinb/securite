from django.contrib.auth.backends import ModelBackend
import logging
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from .models import User

logger = logging.getLogger(__name__)

class UtilisateurAPIBackend(ModelBackend):

    def authenticate(self, request=None,username=None, password=None, **kwargs):
        # Votre logique d'authentification ici
        print(f'Username: {username}, Password: {password}')

        try:
            user = User.objects.using('auth_db').get(username=username)
            print(f'Recherche User dans bd : {user}')
        except User.DoesNotExist:
            print('User non trouvé dans la base de données.')
            return None

        # Vérifiez le mot de passe par rapport à celui stocké dans le compte
        if check_password(password, user.password) and self.user_can_authenticate(user):
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            # Ajouter le token à la session de l'utilisateur
            request.session['access_token'] = access_token
            user.backend = 'custom_auth_service.auth_db.backends.UtilisateurAPIBackend'
            # Mettez à jour l'utilisateur dans la session
            request.session['user_id'] = user.id
            print("request user", request.user)
            return user

        print('Échec de l\'authentification.')
        return None