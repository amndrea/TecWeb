from django.urls import path
from .views import *

app_name = "Workout"

urlpatterns = [

    # URL al quale creo la scheda per un utente
    path('crea_scheda/<int:user_pk>/', SchedaCreateView.as_view(), name="crea_scheda"),

    # URL al quale mostrare la scheda di un utente dalla chiave dell'utente
    path('mostra_scheda/<int:user_pk>/', SchedaDetailView.as_view(), name="mostra_scheda_user"),

    # URL al quale creo un giorno per una scheda
    path('crea_giorno/<int:scheda_pk>/', GiornoSchedaCreateView.as_view(), name="crea_giorno"),

    # URL al quale creare un dettaglio per un giorno e un esercizio
    path('crea_dettaglio/<int:giorno_pk>', DettaglioGiornoCreateView.as_view(), name="crea_dettaglio"),

    # URL al quale modificare il dettaglio di un giorno e un esercizio
    path('modifica_dettaglio/<int:dettaglio_pk>/<int:cosa>/', DettagliGiornoUpdateView.as_view(), name="modifica_dettaglio"),

    # URL ai quali elimino un giorno e dalla scheda di un utente
    path('elimina_giorno/<int:pk>/<int:utente_pk>', DeleteGiorno.as_view(), name="elimina_giorno"),
    path('elimina_dettaglio/<int:pk>/<int:utente_pk>', DeleteDettaglio.as_view(), name="elimina_dettaglio"),

    # URL inutile con il quale visualizzo gli esercizi
    path('acaso/', EsercizioListView.as_view(), name="acaso"),

]
