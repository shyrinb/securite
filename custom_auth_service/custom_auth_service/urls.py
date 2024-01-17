"""auth_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from custom_auth_service.auth_db import views

app_name = 'user_auth'
urlpatterns = [
    path('signup/', views.signup, name='register'),
    path('login/', views.user_login, name='auth_login'),
    path('logout/', views.user_logout, name='logout'),
    path('desinscrire-confirm/<int:contact_id>/', views.desinscrire_confirm, name='desinscrire_confirm'),
    path('desinscrire/<int:contact_id>/', views.desinscrire, name='desinscrire'),
    path('contact-detail/<int:contact_id>/', views.contact_detail,  name='contact_detail'),
    path('change-password/<int:contact_id>/', views.change_password, name='change_password'),
    path('update-profil/<int:contact_id>/', views.update_profile, name='update_profil'),
]