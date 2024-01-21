from django.db import models

class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=10, blank=True)
    email = models.EmailField(blank=True)
    user_id = models.IntegerField(max_length=10, blank=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        db_table = 'annuaire_db_contact'
        app_label = 'annuaire_db'
        
