from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView

from Users.models import MyUser
from .models import *


# --------------------------------------------------------- #
# View per creare una nuova chat tra due utenti
# -------------------------------------------------------- #
def chat(request, u1_pk, u2_pk):
    print("u1 e u2")
    print(u1_pk)
    print(u2_pk)
    chat = Chat.objects.filter(utente_1=u1_pk).filter(utente_2=u2_pk)

    if chat.exists():
        return redirect('Chat:mostra_chat', u1_pk, u2_pk)
    else:
        chat = Chat()
        utente_1 = MyUser.objects.get(pk=u1_pk)
        utente_2 = MyUser.objects.get(pk=u2_pk)
        chat.utente_1 = utente_1
        chat.utente_2 = utente_2
        chat.save()
        chat_pk = chat.pk

    return HttpResponseRedirect(reverse('Chat:mostra_chat', args=[u1_pk, u2_pk]))



def crea_chat(request, u1_pk, u2_pk):
    print("la chat non esiste, la creo")
    chat = Chat()
    utente_1 = MyUser.objects.get(pk=u1_pk)
    utente_2 = MyUser.objects.get(pk=u2_pk)
    chat.utente_1 = utente_1
    chat.utente_2 = utente_2
    chat.save()
    chat_pk = chat.pk
    return HttpResponseRedirect(reverse('Chat:mostra_chat', args=[u1_pk, u2_pk]))

# --------------------------------------------------------- #
# View per visualizzare una chat
# --------------------------------------------------------- #
class ChatDetailView(DetailView):
    model = Chat
    template_name = "Chat/mostra_chat.html"
    context_object_name = "chat"

    def get_object(self, queryset=None):
        print("u1_pk")
        print(self.kwargs.get("u1_pk"))
        chat = Chat.objects.filter(utente_1=self.kwargs.get("u1_pk")).filter(utente_2=self.kwargs.get("u2_pk"))
        return chat



# --------------------------------------------------------- #
# View per inviare un nuovo messaggio
# --------------------------------------------------------- #


# --------------------------------------------------------- #
# View per eliminare una chat
# --------------------------------------------------------- #
