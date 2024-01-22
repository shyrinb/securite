# Projet Securite

## Configuration:

ouvrir le dossier dans un IDE.

## Installation des librairies

installer les librairies via la commande suivante: 


```bash
pip install -r requirements.txt
```

## Configuration des bases de données

Ce projet utilise trois bases de données distinctes : `general`, `auth_db`, et `annuaire_db`. Pour configurer les bases de données, suivez les étapes ci-dessous :

### Dans `securite_projet/settings.py`

1. Ouvrez le fichier `securite_projet/settings.py`.
2. Cherchez la section de configuration de la base de données générale.
3. Mettez à jour les paramètres de connexion de la base de données générale en fonction de votre base de données.

### Dans `annuaire_service/annuaire_service/settings.py`

1. Ouvrez le fichier `annuaire_service/annuaire_service/settings.py`.
2. Recherchez la section de configuration de la base de données annuaire.
3. Mettez à jour les paramètres de connexion de la base de données annuaire en fonction de votre base de données.

### Dans `custom_auth_service/custom_auth_service/settings.py`

1. Ouvrez le fichier `custom_auth_service/custom_auth_service/settings.py`.
2. Recherchez la section de configuration de la base de données d'authentification.
3. Mettez à jour les paramètres de connexion de la base de données d'authentification en fonction de vvotre base de données.

### Appliquer les migrations

Assurez-vous d'appliquer les migrations pour chaque base de données en utilisant les commandes suivantes :

```bash

python manage.py makemigrations
python manage.py migrate
python manage.py migrate --database=auth_db
python manage.py migrate --database=annuaire_db
```
