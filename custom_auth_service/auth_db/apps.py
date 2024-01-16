# auth_service/auth_db/apps.py
from django.apps import AppConfig

class AuthDbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custom_auth_service.auth_db'