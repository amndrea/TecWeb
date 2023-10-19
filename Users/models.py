from django.contrib.auth.models import AbstractUser
from django.db import models

SESSO = [
    ('uomo', 'Uomo'),
    ('donna', 'Donna')
]


# Create your models here.
class MyUser(AbstractUser):
    sesso = models.CharField(max_length=10, choices=SESSO)
    peso = models.FloatField(blank=True, null=True)
    altezza = models.FloatField(blank=True, null=True)
    tipo_abbonamento = models.IntegerField(default=1)
    fine_abbonamento = models.DateField(blank=True, null=True)
    immagine_profilo = models.ImageField(upload_to="fotouser/", blank=True)
    obiettivo = models.CharField(max_length=400, blank=True, null=True)


MyUser._meta.get_field('groups').remote_field.related_name = 'myuser_set'
MyUser._meta.get_field('user_permissions').remote_field.related_name = 'myuser_set'
