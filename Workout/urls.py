from django.urls import path
from .views import *

app_name = "Workout"

urlpatterns = [

    # URL per creare una scheda
    path('creascheda/', SchedaCreateView.as_view(), name="creascheda"),

    # URL per visualizzare tutti gli esercizi da poter inserire in una scheda
    path('listaesercizi/<pk>/', listaesercizi, name="listaesercizi"),

    # URL per inserire il dettaglio di un esercizio in una scheda
    path('creadettaglio/<int:pk_scheda>/<int:pk_esercizio>/', DettaglioCreateView.as_view(), name="crea_dettaglio"),


]

# DeleteEsercizio
# RiempiDbEsercizio
