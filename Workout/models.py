from django.db import models

DISTRETTO = [
    ('spalle', 'Spale'),
    ('pettorali', 'Pettorali'),
    ('dorsali', 'Dorsali'),
    ('gambe', 'Gambe'),
    ('braccia', 'Braccia'),
    ('all', 'All')
]


class Esercizio(models.Model):
    nome = models.CharField(max_length=40)
    descrizione = models.CharField(max_length=450, blank=True)
    distretto_target = models.CharField(max_length=20, choices=DISTRETTO, default='All')
    immagine = models.ImageField(upload_to="immagini_es/", blank=True)

    def __str__(self):
        return self.nome + " " + self.descrizione
        
    class Meta:
        verbose_name_plural = "Esercizi"


class Scheda(models.Model):
    my_user = models.ForeignKey('Users.MyUser', on_delete=models.CASCADE, db_column='my_user_id')
    tipologia = models.CharField(max_length=20)
    descrizione = models.CharField(max_length=250)
    data_inizio = models.DateField(null=True, blank=True)
    data_fine = models.DateField(null=True, blank=True)

    def __str__(self):
        return "Tipologia scheda: " + self.tipologia + " Descrizione :" + self.descrizione

    class Meta:
        verbose_name_plural = "Schede"


# Classe che mette in relazione una scheda con i giorni che la compongono
class GiornoScheda(models.Model):
    giorno = models.IntegerField(default=1)
    Scheda = models.ForeignKey(Scheda, on_delete=models.CASCADE)
    descrizione_giorno = models.CharField(max_length=300, blank=True)


class DettaglioEsercizioGiorno(models.Model):
    giorno = models.ForeignKey(GiornoScheda, on_delete=models.CASCADE)
    esercizio = models.ForeignKey(Esercizio, on_delete=models.CASCADE)

    serie = models.IntegerField(default=0)
    ripetizioni = models.IntegerField(default=0)
    recupero = models.IntegerField(default=0)
    descrizione = models.CharField(max_length=350, blank=True)
