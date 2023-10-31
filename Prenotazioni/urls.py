from django.urls import path
from .views import *

app_name = "Prenotazioni"

urlpatterns = [

    # URL al quale mostro il calendario a partire dal mese corrente
    path("mostra_calendario/<int:user_pk>/",mostra_calendario,name="calendario"),

    # URL al quale visualizzo gli orari prenotabili di un dato giorno
    path("mostra_giorno/<int:year>/<int:month>/<int:day>/", mostra_giorno, name="mostra_giorno"),

    # URL al quale effettuo una prenotazione per un orario
    path("prenota/<str:orario>/<int:giorno_pk>/<int:utente_pk>/", effettua_prenotazione, name="prenota"),

]
