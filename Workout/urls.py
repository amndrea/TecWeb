from django.urls import path
from .views import *

app_name = "Workout"

urlpatterns = [

    # URL al quale creo la scheda per un utente
    path('crea_scheda/<int:user_pk>/', SchedaCreateView.as_view(), name="crea_scheda"),

    #  TODO da completare la view URL al quale mostro la scheda completa di un utente
    path('mostra_scheda/<int:user_pk>/', SchedaDetailView.as_view(), name="mosta_scheda_user"),

    # URL al quale creo un giorno per una scheda
    path('crea_giorno/<int:scheda_pk>/', GiornoSchedaCreateView.as_view(), name="crea_giorno"),

    path('crea_dettaglio/<int:giorno_pk>',DettaglioGiornoCreateView.as_view(), name="crea_dettaglio"),

    # URL inutile con il quale visualizzo gli esercizi
    path('acaso/', EsercizioListView.as_view(), name="acaso"),

]
