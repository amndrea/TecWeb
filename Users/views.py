from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import PermissionRequiredMixin
from braces.views import GroupRequiredMixin

from .models import MyUser
from .forms import CreaUtenteCrispyForms, CreaNutrizionista, CreaPersonalTrainer

import datetime


# Classe che implementa la creazione di un utente grazie alla classe CreaUtenteCrispyForms
class UserCreateView(CreateView):
    form_class = CreaUtenteCrispyForms
    template_name = "Users/crea_utente.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        form.instance.fine_abbonamento = datetime.date.today()
        form.instance.tipo_abbonamento = 0
        return super().form_valid(form)


class NutrizionistaCreateView(PermissionRequiredMixin, UserCreateView):
    permission_required = "is_staff"
    form_class = CreaNutrizionista

    def form_valid(self, form):
        form.instance.tipo_abbonamento = 2


class PersonalTrainerCreateView(PermissionRequiredMixin, UserCreateView):
    permission_required = "is_staff"
    form_class = CreaPersonalTrainer

    def form_valid(self, form):
        form.instance.tipo_abbonamento = 2


class UtentiListView(GroupRequiredMixin, ListView):
    group_required = ["nutrizionista", "pt"]
    model = MyUser
    template_name = "Users/lista_utenti.html"

    def get_queryset(self):
        gruppo_pt = Group.objects.get(name="pt")
        gruppo_nutrizionista = Group.objects.get(name="nutrizionista")
        queryset = MyUser.objects.exclude(groups=gruppo_pt).exclude(groups=gruppo_nutrizionista)
        queryset = queryset.exclude(is_superuser=True)
        return queryset
