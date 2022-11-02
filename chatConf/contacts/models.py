from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class ContactsList(models.Model):
    user = models.OneToOneField(
        User, 
        related_name='contacts_list_owner', 
        on_delete=models.CASCADE
        )
    contacts = models.ManyToManyField(
        User, 
        related_name='contacts', 
        blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'user_contacts_list'