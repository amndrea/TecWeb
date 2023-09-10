from django.urls import path
from Diet.views import *
from .initcmd import *

app_name = "Diet"

urlpatterns = [

    # URL al quale creo i dati generici di una dieta
    path('creadieta/', DietaCreateView.as_view(), name="crea_dieta"),

    # URL al quale visualizzo gli alimenti da inserire nel dettaglio di una dieta
    path('mostradettaglio/<pk>/', mostra_dettaglio_dieta, name="mostra_dettaglio"),

    # URL al quale inserisco le caratteristiche di un alimento in una dieta come pasto e quantita
    path('creadettaglio/<int:dieta_pk>/<int:alimento_pk>/', DettaglioDietaCreateView.as_view(), name="crea_dettaglio"),

    # URL al quale mostro tutti i dettagli di una dieta
    path('mostradieta/<pk>/', MostraDietaCompleta.as_view(), name="mostra_dieta")
]


#svuota_tabelle()
#salva_alimenti_su_file()
#carica_alimenti()

