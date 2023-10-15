from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from Users.models import MyUser
from .forms import *


class SchedaCreateView(CreateView):
    template_name = "Workout/crea_scheda.html"
    form_class = SchedaCreateForm

    def get_user(self):
        user = MyUser.objects.get(pk=self.kwargs.get('user_pk'))
        return user

    def form_valid(self, form):
        form.instance.my_user=self.get_user()

    def get_success_url(self):
        def get_success_url(self):
            ctx = self.get_context_data()
            pk = ctx["object"].pk

            return reverse_lazy("Diet:mostra_giorni", kwargs={'dieta_pk': pk})
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
            print(Exception)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        scheda = self.get_object()
        my_user = self.get_user()
        context['my_user'] = my_user
        return context

        """
        giorni_dieta = GiornoDieta.objects.filter(dieta=dieta)
        for giorno_dieta in giorni_dieta:
            dettagli = DettaglioGiornoAlimento.objects.filter(giorno=giorno_dieta)
            dett.extend(dettagli)
        context['dettagli'] = dett
        context['giorni_dieta'] = giorni_dieta
        context['my_user'] = self.get_user()
        context['dieta'] = dieta
        return context
    """



# Funzione inutile, usata solo nella fase di testing per visualizzare gli esercizi
class EsercizioListView(ListView):
    model = Esercizio
    template_name = "Workout/lista_esercizi.html"
