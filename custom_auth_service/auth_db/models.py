# auth_db/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomGroup(Group):
    pass

class CustomPermission(Permission):
    pass

class User(AbstractUser):

    class Status(models.IntegerChoices):
        utilisateur = 0
        admin =1
        superadmin =2
    
    groups = models.ManyToManyField(CustomGroup, blank=True, related_name='user_groups')
    user_permissions = models.ManyToManyField(CustomPermission, blank=True, related_name='user_permissions')
    contact_relation = models.ForeignKey('annuaire_db.Contact', on_delete=models.SET_NULL, related_name='contact_account', null=True, blank=True)
    status = models.IntegerField(
        choices = Status.choices, 
        default = Status.utilisateur,
    )
    
    def __str__(self):
        return f'{self.id}'

    class Meta:
        db_table = 'auth_db_user'
        app_label = 'auth_db'
        

class Historique(models.Model):
    ACTION_CHOICES = [
        ('creation', 'Création'),
        ('suppression', 'Suppression'),
        ('mise_a_jour', 'Mise à jour'),
        ('connexion', 'Connexion'),
        ('deconnexion', 'Déconnexion'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    commentaire = models.CharField(max_length=50, blank=True)
    action= models.CharField(max_length=50, choices=ACTION_CHOICES, blank=True)
    timestamp = models.DateTimeField(auto_now=True)