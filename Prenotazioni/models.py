from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Giorno(models.Model):
    anno = models.IntegerField()
    mese = models.IntegerField()
    giorno = models.IntegerField()

class Prenotazione(models.Model):
    giorno = models.ForeignKey(Giorno, on_delete=models.CASCADE)
    user = models.ForeignKey('Users.MyUser', on_delete=models.CASCADE)
    ora = models.IntegerField( validators=[MinValueValidator(8), MaxValueValidator(20)])




