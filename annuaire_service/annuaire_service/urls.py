"""annuaire_service URL Configuration

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
from annuaire_service.annuaire_db import views
app_name = 'annuaire_user'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('search-contact/', views.search_contact, name='search_contact'),

    path('go-contact/', views.go_to_search, name='go_to_search'),
    # Ajout contact 
    path('add-contact', views.add_contact, name='add_contact'),
    # Proumouvoir utilisateur
    path('promove-contact/<int:contact_id>/',views.promove_contact,name='promove_contact'),
    path('update-contact/<int:contact_id>/', views.update_contact, name='update_contact'),
    # Retrograder utilisateur   
    path('retrograde-contact/<int:contact_id>/', views.retrograde_contact, name='retrograde_contact'),  
    path('delete-contact/<int:contact_id>/', views.delete_contact, name='delete_contact'),
    path('accounts/', views.contact, name='account_list') # voir tous les utilisateurs
]
