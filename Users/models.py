from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class MyUser(AbstractUser):
    peso = models.FloatField(blank=True, null=True)
    altezza = models.FloatField(blank=True, null=True)
    tipo_abbonamento = models.IntegerField(default=1)
    fine_abbonamento = models.DateField()

