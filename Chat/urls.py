from django.urls import path
from .views import *

app_name = "Chat"

urlpatterns = [

    # URL al quale mostro o creo una chat
    path("chat/<int:u1_pk>/<int:u2_pk>/",chat,name="chat"),

    # URL al quale due utenti possono chattare
    path("mostra_chat/<int:u1_pk>/<int:u2_pk>/", chat_utenti, name="mostra_chat"),

]
