from django.db import models

SCELTA_PASTI = [
    ('colazione', 'Colazione'),
    ('spuntino', 'Spuntino'),
    ('pranzo', 'Pranzo'),
    ('merenda', 'Merenda'),
    ('cena', 'Cena')
]

SCELTA_GIORNI = [
    ('lunedi', 'Lunedi'),
    ('martedi', 'Martedi'),
    ('mercoledi', 'Mercoledi'),
    ('giovedi', 'Giovedi'),
    ('venerdi', 'Venerdi'),
    ('sgarro', 'Sgarro'),
]


class Alimento(models.Model):
    nome = models.CharField(max_length=35, unique=True)
    proteine = models.FloatField(default=0)
    carboidrati = models.FloatField(default=0)
    grassi = models.FloatField(default=0)
    cal = models.FloatField(default=0)

    def __str__(self):
        return self.nome + " Proteine " + str(self.proteine) + " Carboidrati " + str(self.carboidrati) + " Grassi " + str(self.grassi) + " Calorie " + str(self.cal)

    def get_macro(self):
        return "Calorie = " + str(self.cal) + " Proteine = " + str(
            self.proteine) + " Carboidrati = " + str(self.carboidrati) + " Grassi = " + str(self.grassi)

    class Meta:
        verbose_name_plural = "Alimenti"
        ordering = ['nome']


class Dieta(models.Model):
    tipologia = models.CharField(max_length=30)
    descrizione = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return str(self.pk) + "  "+self.tipologia+ " "+ self.descrizione


class DettaglioDieta(models.Model):
    alimento = models.ForeignKey(Alimento, on_delete=models.CASCADE)
    dieta = models.ForeignKey(Dieta, on_delete=models.CASCADE)

    giorni = models.CharField(max_length=10, choices=SCELTA_GIORNI, default='Colazione')
    pasto = models.CharField(max_length=10, choices=SCELTA_PASTI, default='Sgarro')
    quantita = models.IntegerField(default=0)

    class Meta:
        ordering = ['giorni', 'pasto']
