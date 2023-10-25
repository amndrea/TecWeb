from django.urls import path
from .views import *

app_name = "Chat"

urlpatterns = [

    # URL al quale mostro o creo una chat tra due utenti
    path("chat/<int:u1_pk>/<int:u2_pk>/",chat,name="chat"),

    # URL al quale mostro una chat tra due utenti
    path("mostra_chat/<int:u1_pk>/<int:u2_pk>/", ChatDetailView.as_view(), name="mostra_chat")

]
