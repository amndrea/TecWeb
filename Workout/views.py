from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from Users.models import MyUser
from .forms import *


# ------------------------------------------------------------------------- #
# View per la creazione della scheda di un utente
# ------------------------------------------------------------------------- #
class SchedaCreateView(CreateView):
    template_name = "Workout/crea_scheda.html"
    form_class = SchedaCreateForm

    def get_user(self):
        my_user = MyUser.objects.get(pk=self.kwargs.get('user_pk'))
        return my_user

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['my_user'] = self.get_user()
        return context

    def form_valid(self, form):
        form.instance.my_user = self.get_user()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("home_login")
# ------------------------------------------------------------------------- #
# ------------------------------------------------------------------------- #


# ------------------------------------------------------------------------- #
# View per la visualizzazione della scheda completa di un untente
# ------------------------------------------------------------------------- #
class SchedaDetailView(DetailView):
    model = Scheda
    template_name = "Workout/mostraschedautente.html"
    context_object_name = "scheda"

    def get_user(self):
        user = MyUser.objects.get(pk=self.kwargs.get('user_pk'))
        return user

    def get_object(self, queryset=None):
        try:
            user = self.get_user()
            scheda = Scheda.objects.filter(my_user=user).latest('pk')
            return scheda
        except Scheda.DoesNotExist:
            print("la scheda non esiste")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dett = []
        giorni_scheda = GiornoScheda.objects.filter(Scheda=self.get_object())
        for giorno_scheda in giorni_scheda:
            dettagli = DettaglioEsercizioGiorno.objects.filter(giorno=giorno_scheda)
            dett.extend(dettagli)
        
        context['my_user'] = self.get_user()
        context['giorni_scheda'] = giorni_scheda
        context['dettagli'] = dett
        context['scheda'] = self.get_object()
        return context
# ------------------------------------------------------------------------- #
# ------------------------------------------------------------------------- #


# ------------------------------------------------------------------------- #
# Classe inutile, usata solo nella fase di testing per visualizzare gli esercizi
# ------------------------------------------------------------------------- #
class EsercizioListView(ListView):
    model = Esercizio
    template_name = "Workout/lista_esercizi.html"


# ------------------------------------------------------------------------- #
# View per la creazione di un giorno per scheda
# ------------------------------------------------------------------------- #
class GiornoSchedaCreateView(CreateView):
    model = GiornoScheda
    template_name = "Workout/crea_giorno.html"
    form_class = GiornoCreateForm

    def form_valid(self, form):
        form.instance.Scheda = self.get_scheda()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['scheda'] = self.get_scheda()
        return context

    def get_success_url(self):
        return reverse_lazy("Workout:crea_dettaglio", kwargs={"giorno_pk": self.object.pk})

    def get_scheda(self):
        scheda = Scheda.objects.get(pk=self.kwargs.get("scheda_pk"))
        return scheda
# ------------------------------------------------------------------------- #
# ------------------------------------------------------------------------- #
class DettaglioGiornoCreateView(CreateView):
    template_name = "Workout/crea_dettaglio.html"
    form_class = DettaglioGiornoEsercizioForm

    def form_valid(self, form):
        form.instance.giorno = self.get_giorno()
        return super().form_valid(form)

    def get_giorno(self):
        giorno = GiornoScheda.objects.get(pk=self.kwargs.get("giorno_pk"))
        return giorno

    def get_success_url(self):
        return reverse_lazy("Workout:mosta_scheda_user", kwargs={'user_pk':self.get_giorno().Scheda.my_user.pk})


# ------------------------------------------------------------------------- #
#    View per modificare un dettaglio di un esercizio in un giorno
# ------------------------------------------------------------------------- #
class DettagliGiornoUpdateView(UpdateView):
    model = DettaglioEsercizioGiorno
    form_class = DettagliGiornoEsercizioForm
    template_name = 'Workout/modifica_dettaglio.html'

    