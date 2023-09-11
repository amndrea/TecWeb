from django.db import models

DISTRETTO = [
    ('spalle', 'Spale'),
    ('pettorali', 'Pettorali'),
    ('dorsali', 'Dorsali'),
    ('gambe', 'Gambe'),
    ('braccia', 'Braccia'),
    ('all','All')
]

NUMERO_GIORNI = [('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7)]


class Esercizio(models.Model):
    nome = models.CharField(max_length=40)
    descrizione = models.CharField(max_length=450, blank=True)
    distretto_target = models.CharField(max_length=20, choices=DISTRETTO, default='All')
    immagine = models.ImageField(upload_to="exercises_image", blank=True)

    def __str__(self):
        return self.nome + " " + self.descrizione
        
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
    giorno = models.IntegerField(default=1, choices=NUMERO_GIORNI)
    serie = models.IntegerField(default=0)
    ripetizioni = models.IntegerField(default=0)
    recupero = models.IntegerField(default=0)
    descrizione = models.CharField(max_length=350, blank=True)

    def __str__(self):
        pass
