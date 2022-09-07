from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Room(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created', '-updated']

    def __str__(self):
        return self.name


class Message(models.Model):
    body = models.TextField() # null je defaultně False a blank také False
    room = models.ForeignKey(Room, on_delete=models.CASCADE) # on_delete=models.CASCADE = když se smaže room tak se smažou i lavinově zprávy
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True) # zazanamenej čas při vytvoření zprávy auto_now_add aniž bychom na created šáhli tak jakmile se vytvoří zpráva tak Django zazanmená aktuální čas
                                                      # vytvoření zprávy
    updated = models.DateTimeField(auto_now=True) # auto_now = při jakékoliv změněn zazanammenj čas

    class Meta:
        ordering = ['-created','-updated'] # bez minus je v defaultu ASC, s minusem nastavím DESC

    def __str__(self):
        return self.body[0:50] # zobrazí se mi prvních 50 znaků, abych to neměl tak dlouhý

