from django.db import models


# Create your models here.
class Chat(models.Model):
    utente_1 = models.ForeignKey('Users.MyUser', on_delete=models.CASCADE, related_name="utente_1")
    utente_2 = models.ForeignKey('Users.MyUser', on_delete=models.CASCADE, related_name="utente_2")


class Messaggio(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    testo = models.CharField(max_length=500)
    letto = models.BooleanField(default=False)
    data = models.DateTimeField(auto_now_add=True)
    mittente = models.ForeignKey('Users.MyUser', on_delete=models.CASCADE)
