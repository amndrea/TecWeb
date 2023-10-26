from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView
from .forms import *
from Users.models import MyUser
from .models import *


# ---------------------------------------------------------------------------- #
# View che crea una chat tra due utenti se questa non esiste, altrimenti
# redireziona alla pagina dove mostra la chat se questa esiste, chiamano
# la DetailView associata all'url mostra_chat
# ---------------------------------------------------------------------------- #
def chat(request, u1_pk, u2_pk):
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




# --------------------------------------------------------- #
# View per visualizzare una chat
# --------------------------------------------------------- #
class ChatDetailView(DetailView):
    model = Chat
    template_name = "Chat/mostra_chat.html"
    context_object_name = "chat"

    def get_object(self, queryset=None):
        chat = Chat.objects.filter(utente_1=self.kwargs.get("u1_pk")).filter(utente_2=self.kwargs.get("u2_pk")).latest("pk")
        return chat

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chat = self.get_object()
        messaggi = Messaggio.objects.filter(chat=chat).order_by("data")
        context['messaggi'] = messaggi
        return context


# --------------------------------------------------------- #
# View per inserire un nuovo messaggio in una chat
# --------------------------------------------------------- #
class MessaggioCreateView(CreateView):
    template_name = "Chat/invia_messaggio.html"
    form_class = MessaggioCreateForm

    def get_chat(self):
        chat = Chat.objects.filter(utente_1=self.kwargs.get("u1_pk")).filter(utente_2=self.kwargs.get("u2_pk")).latest("pk")
        return chat

    def form_valid(self, form):
        chat = self.get_chat()
        form.instance.chat = chat.pk
        return super().form_valid(form)