from braces.views import GroupRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from Users.models import MyUser
from .forms import *


# ------------------------------------------------------------------------- #
# View per la creazione della scheda di un utente
# ------------------------------------------------------------------------- #
class SchedaCreateView(GroupRequiredMixin, CreateView):
    template_name = "Workout/crea_scheda.html"
    form_class = SchedaCreateForm
    group_required = ["pt"]
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
class SchedaDetailView(LoginRequiredMixin, DetailView):
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
class EsercizioListView(LoginRequiredMixin, ListView):
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
class DettaglioGiornoCreateView(GroupRequiredMixin, CreateView):
    template_name = "Workout/crea_dettaglio.html"
    form_class = DettaglioGiornoEsercizioForm
    group_required = ["pt"]
    def form_valid(self, form):
        form.instance.giorno = self.get_giorno()
        return super().form_valid(form)

    def get_giorno(self):
        giorno = GiornoScheda.objects.get(pk=self.kwargs.get("giorno_pk"))
        return giorno

    def get_success_url(self):
        return reverse_lazy("Workout:mostra_scheda_user", kwargs={'user_pk': self.get_giorno().Scheda.my_user.pk})


# ------------------------------------------------------------------------- #
#    View per modificare un dettaglio di un esercizio in un giorno
# ------------------------------------------------------------------------- #
class DettagliGiornoUpdateView(GroupRequiredMixin, UpdateView):
    model = DettaglioEsercizioGiorno
    template_name = 'Workout/modifica_dettaglio.html'
    context_object_name = 'dettaglio'
    group_required = ["pt"]

    def get_object(self, queryset=None):
        dettaglio = DettaglioEsercizioGiorno.objects.get(pk=self.kwargs.get("dettaglio_pk"))
        return dettaglio

    def get_form_class(self):
        cosa = self.kwargs.get("cosa")
        # form per modificare le serie
        if cosa == 1:
            return DettaglioUpdateSerie
        # form per modificare le ripetizioni
        elif cosa == 2:
            return DettaglioUpdateRipetizioni
        # form per modificare il tempo di recupero
        else:
            return DettaglioUpdateRecupero

    def get_success_url(self):
        dettaglio = self.get_object()
        giorno_scheda = dettaglio.giorno
        utente_pk = giorno_scheda.Scheda.my_user.pk
        return reverse_lazy("Workout:mostra_scheda_user", kwargs={'user_pk': utente_pk})


# ------------------------------------------------------------------------- #
# View per le eliminazioni di un giorno da una scheda o di un dettaglio da
# una scheda, entrambe le view ereditano dal DeleteOggettoView
# ------------------------------------------------------------------------- #
class DeleteOggettoView(GroupRequiredMixin,DeleteView):
    template_name = "Workout/delete.html"
    group_required = ["pt"]

    def get_success_url(self):
        return reverse("Workout:mostra_scheda_user", kwargs={'user_pk': self.kwargs.get("utente_pk")})


class DeleteGiorno( DeleteOggettoView):
    group_required = ["pt"]
    model = GiornoScheda

    def get_object(self, queryset=None):
        giorno = GiornoScheda.objects.get(pk=self.kwargs.get("pk"))
        return giorno


class DeleteDettaglio( DeleteOggettoView):
    model = DettaglioEsercizioGiorno


    def get_object(self, queryset=None):
        dettaglio = DettaglioEsercizioGiorno.objects.get(pk=self.kwargs.get("pk"))
        return dettaglio
