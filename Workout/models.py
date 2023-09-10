from django.db import models


class Esercizio(models.Model):
    nome = models.CharField(max_length=40)
    descrizione = models.CharField(max_length=450, blank=True)
    immagine = models.ImageField(upload_to="exercises_image", blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Esercizi"


class Scheda(models.Model):
    tipologia = models.CharField(max_length=20)
    descrizione = models.CharField(max_length=250)
    # Manca il riferimento all'utente
    # Manca il riferimento al pt

    def __str__(self):
        return "Tipologia scheda: " + self.tipologia + " Descrizione :" + self.descrizione

    class Meta:
        verbose_name_plural = "Schede"


class DettaglioEsercizioScheda(models.Model):
    scheda = models.ForeignKey(Scheda, on_delete=models.CASCADE)
    esercizio = models.ForeignKey(Esercizio, on_delete=models.CASCADE)
    giorno = models.IntegerField(default=0)
    serie = models.IntegerField(default=0)
    ripetizioni = models.IntegerField(default=0)
    recupero = models.IntegerField(default=0)
    descrizione = models.CharField(max_length=350, blank=True)

    def __str__(self):
        pass

