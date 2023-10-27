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

    # URL al quale visualizzo i pt e i nutrizionisti da cliente per poterci chattare
    path('lista_staff/',StaffListView.as_view(),name="lista_staff"),

    # URL al quale un utente visualizza la propria situazione personale
    path('situazione/<int:user_pk>/',UtenteDetailView.as_view(),name="situazione"),

    # URL al quale un utente può modificare la sua situazione personale
    path('edit/<int:user_pk>/<int:cosa_editare>/', UtenteUpdateView.as_view(),name="edit"),

]
