from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone

SCELTA_PASTI = [
    ('1', 'Colazione'),
    ('2', 'Spuntino'),
    ('3', 'Pranzo'),
    ('4', 'Merenda'),
    ('5', 'Cena')
]


class Alimento(models.Model):
    nome = models.CharField(max_length=35, unique=True)
    proteine = models.FloatField(default=0)
    carboidrati = models.FloatField(default=0)
    grassi = models.FloatField(default=0)
    cal = models.FloatField(default=0)

    # Metodo che utilizzo per visualizzare l'oggetto nella pagina admin
    def __str__(self):
        return self.nome + " Proteine " + str(self.proteine) + " Carboidrati " + str(
            self.carboidrati) + " Grassi " + str(self.grassi) + " Calorie " + str(self.cal)

    def get_macro(self):
        return "Calorie = " + str(self.cal) + " Proteine = " + str(
            self.proteine) + " Carboidrati = " + str(self.carboidrati) + " Grassi = " + str(self.grassi)

    def get_macro_float(self):
        return (self.proteine, self.carboidrati, self.grassi, self.cal)

    class Meta:
        verbose_name_plural = "Alimenti"
        ordering = ['nome']


class Dieta(models.Model):
    my_user = models.ForeignKey('Users.MyUser', on_delete=models.CASCADE, db_column='my_user_id')
    tipologia = models.CharField(max_length=30)
    descrizione = models.CharField(max_length=300, blank=True)
    data_inizio = models.DateField(null=True, blank=True)
    data_fine = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.pk) + "  " + self.tipologia + " " + self.descrizione


class GiornoDieta(models.Model):
    giorno = models.IntegerField(unique=True, default=1, auto_created=True)
    dieta = models.ForeignKey(Dieta, on_delete=models.CASCADE)
    proteine = models.FloatField(default=0)
    carboidrati = models.FloatField(default=0)
    grassi = models.FloatField(default=0)
    cal = models.FloatField(default=0)

    def get_macro(self):
        return "Calorie = " + str(self.cal) + " Proteine = " + str(
            self.proteine) + " Carboidrati = " + str(self.carboidrati) + " Grassi = " + str(self.grassi)

    def get_macro_float(self):
        return (self.proteine, self.carboidrati, self.grassi, self.cal)

    def update_macro(self, macro_nuovo_alimento):
        # ottengo una tupla con i macro attuali + la somma dei macro del nuovo alimento
        nuovi_macro = tuple(x + y for x, y in zip(macro_nuovo_alimento, self.get_macro_float()))
        self.proteine, self.carboidrati, self.grassi, self.cal = nuovi_macro
        self.save()


class DettaglioGiornoAlimento(models.Model):
    alimento = models.ForeignKey(Alimento, on_delete=models.CASCADE)
    giorno = models.ForeignKey(GiornoDieta, on_delete=models.CASCADE)
    # dieta = models.ForeignKey(Dieta, on_delete=models.CASCADE)

    pasto = models.CharField(max_length=10, choices=SCELTA_PASTI, default='Sgarro')
    quantita = models.IntegerField(default=0)

    class Meta:
        ordering = ['pasto']
