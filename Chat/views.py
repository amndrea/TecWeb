from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from Users.models import MyUser
from .models import *


# ---------------------------------------------------------------------------- #
# View che crea una chat tra due utenti se questa non esiste, altrimenti
# re-direziona alla pagina dove mostra la chat se questa esiste, chiamano
# la DetailView associata all url mostra_chat
# ---------------------------------------------------------------------------- #
@login_required
def chat(request, u1_pk, u2_pk):
    chat_i = Chat.objects.filter(utente_1=u1_pk).filter(utente_2=u2_pk).first()
    if not chat_i:
        chat_i = Chat()
        utente_1 = MyUser.objects.get(pk=u1_pk)
        utente_2 = MyUser.objects.get(pk=u2_pk)
        chat_i.utente_1 = utente_1
        chat_i.utente_2 = utente_2
        chat_i.save()
    return HttpResponseRedirect(reverse('Chat:mostra_chat', args=[u1_pk, u2_pk]))


# ---------------------------------------------------------------------------- #
# View per visualizzare i messaggi tra due utenti
# all'invio del form, viene richiamata la view, e il messaggio viene inserito
# ---------------------------------------------------------------------------- #
@login_required
def chat_utenti(request, u1_pk, u2_pk):
    if request.method == "POST":
        testo = request.POST.get('messaggio')
        messaggio = Messaggio()
        messaggio.chat = Chat.objects.filter(utente_1=u1_pk).filter(utente_2=u2_pk).first()
        messaggio.testo = testo
        messaggio.mittente = request.user
        messaggio.save()

    chat = Chat.objects.filter(utente_1=u1_pk).filter(utente_2=u2_pk).first()
    messaggi = Messaggio.objects.filter(chat=chat).order_by("-data")

    ctx = {"chat": chat, "messaggi": messaggi}

    return render(request, template_name="Chat/mostra_chat.html", context=ctx)
