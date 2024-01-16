#annuaire_service/annuaire_service/routers.py
import logging

class AnnuaireRouter:
    app_name = 'annuaire_db'

    def db_for_read(self, model, **hints):
        if model._meta.app_label == self.app_name:
            return 'annuaire_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == self.app_name:
            return 'annuaire_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        logger = logging.getLogger('django')
        logger.info(f'allow_migrate: db={db}, app_label={app_label}, model_name={model_name}')
        
        if app_label == self.app_name:
            return db == 'annuaire_db'
        return None
