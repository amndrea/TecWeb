from django.urls import path
from .views import *

app_name = "Users"

urlpatterns = [
    # URL al quale un utente tenta la registrazione
    path('creautente/', UserCreateView.as_view(), name="crea_utente"),

    # URL al quale l'admin crea un nutrizionista
    path('creanutrizionista/', NutrizionistaCreateView.as_view(), name="crea_nutrizionista"),

    # URL al quale l'admin crea un personaltrainer
    path('creapt/', PersonalTrainerCreateView.as_view(), name="creaa_pt"),

    # URL al quale un pt o un nutrizionista visualizzano la lista dei clienti
    path('listautenti/', UtentiListView.as_view(), name="listautenti"),
]
