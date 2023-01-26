from django.db import models
from django.contrib.auth.models import User # importuji User model z django.contrib.auth.models, který má v sobě first name, last name, e-mail
from django.db.models.signals import post_save # importuji post_save signal, který se spustí po vytvoření uživatele
from django.dispatch import receiver # importuji receiver, který bude přijímat signál


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about_me = models.TextField(null=True, blank=True)
    photo = models.TextField(null=True, blank=True)
    last_seen = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

class OnlineUsers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

"""
@receiver(post_save, sender=User) # receiver přijímá signál post_save, který se spustí po vytvoření uživatele - pokud se User přejmenuje tak si ho rovním ulžožím pod jiným jménem, ale vím, že je to on
def save_user_profile(sender, instance, **kwargs):# funkce save_user_profile, která přijímá signál post_save, který se spustí po vytvoření uživatele
    instance.profile.save() # instance.profile.save() = vytvoří profil uživatele
"""

