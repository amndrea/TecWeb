from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from braces.views import GroupRequiredMixin
from .forms import *
import datetime
from datetime import datetime as d


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
        return super().form_valid(form)


class PersonalTrainerCreateView(PermissionRequiredMixin, UserCreateView):
    permission_required = "is_staff"
    form_class = CreaPersonalTrainer

    def form_valid(self, form):
        form.instance.tipo_abbonamento = 2
        return super().form_valid(form)


# ------------------------------------------------------------------------------------------- #
# View per visualizzare tutti gli utenti che non sono ne pt ne nutrizionisti ne superuser
# ------------------------------------------------------------------------------------------- #
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


# ------------------------------------------------------------------------------------------- #
# View per visualizzare la situazione personale di un utente
# ------------------------------------------------------------------------------------------- #
class UtenteDetailView(LoginRequiredMixin, DetailView):
    model = MyUser
    template_name = "Users/situazione.html"
    context_object_name = "user"

    def get_object(self, queryset=None):
        user = MyUser.objects.get(pk=self.kwargs.get("user_pk"))
        print(user.fine_abbonamento)
        return user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = d.now().date()
        print("data")
        print(data)
        context['data'] = data
        return context


# ------------------------------------------------------------------------------------------- #
# View generica per modificare un utente
# ------------------------------------------------------------------------------------------- #

class UtenteUpdateView(LoginRequiredMixin, UpdateView):
    model = MyUser
    template_name = "Users/edit_profile.html"

    def get_object(self, queryset=None):
        user = MyUser.objects.get(pk=self.kwargs.get("user_pk"))
        return user

    def get_form_class(self):
        cosa = self.kwargs.get("cosa_editare")
        # restituisco il form per l'edit completo dell'utente
        if cosa == 1:
            return UtenteUpdateform
        # restituisco il form per l'edit del peso
        if cosa == 2:
            return UtenteUpdatePeso
        # restituisco il form per l'edit dell'altezza
        if cosa == 3:
            return UtenteUpdateAltezza
        if cosa == 4:
            return UtenteUpdateFoto
        if cosa == 5:
            return UtenteUpdateAbbonamento

    def get_success_url(self):
        return reverse_lazy("Users:situazione",  kwargs={'user_pk':self.get_object().pk})


# ------------------------------------------------------------------------------------------- #
# View per visualizzare gli utenti che sono nutrizionisti o personal trainer
# ------------------------------------------------------------------------------------------- #
class StaffListView(LoginRequiredMixin, ListView):
    model = MyUser
    template_name = "Users/lista_staff.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        gruppo_pt = Group.objects.get(name="pt")
        gruppo_nutrizionista = Group.objects.get(name="nutrizionista")

        context['pt'] = MyUser.objects.filter(groups__in=[gruppo_pt])
        context['nutrizionista'] = MyUser.objects.filter(groups__in=[ gruppo_nutrizionista])

        return context


class AbbonamentoEditView(GroupRequiredMixin, UpdateView):
    model = MyUser
    template_name = "Users/edit_abbonamento.html"
    group_required = ["nutrizionista", "pt"]

    def get_object(self, queryset=None):
        user = MyUser.objects.get(pk=self.kwargs.get("user_pk"))
        return user
