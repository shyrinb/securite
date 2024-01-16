# securite_projet/urls.py

from django.contrib import admin
from django.urls import path, include  # Ajoutez l'import pour la fonction include
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test
from custom_auth_service.auth_db.models import User
from custom_auth_service.auth_db.views import user_login
from annuaire_service.annuaire_db.views import home

urlpatterns = [
    path('', lambda request: redirect('user_auth:register')),
    path('admin/', admin.site.urls),
    path('annuaire/', include(('annuaire_service.annuaire_service.urls', 'annuaire_user'), namespace='annuaire_user')),
    path('auth/', include(('custom_auth_service.custom_auth_service.urls', 'user_auth'), namespace='user_auth')),

    path('annuaire/home/',home, name='annuaire_home'),
    path('auth/login/', user_login, name='auth_login'),
]
