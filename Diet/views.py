from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from Users.models import MyUser
from .forms import *


# ------------------------------------------------------------------ #
# View per la creazione di una dieta
# ------------------------------------------------------------------ #
class DietaCreateView(CreateView):
    template_name = 'Diet/crea_dieta.html'
    form_class = InsertDietaCrispyForm

    def get_user(self):
        user_pk = self.kwargs.get('utente_pk')
        user = MyUser.objects.get(pk=user_pk)
        return user

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['my_user'] = self.get_user()
        return context


    def form_valid(self, form):
        form.instance.my_user = self.get_user()
        return super().form_valid(form)

    def get_success_url(self):
        ctx = self.get_context_data()
        pk = ctx["object"].pk

        return reverse_lazy("home_login")

# ------------------------------------------------------------------ #
# View per la modifica di una dieta
# ------------------------------------------------------------------ #
class DietaEditView(UpdateView):
    model = Dieta
    form_class = DietaUpdateForm
    template_name = 'Diet/modifica_dieta.html'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('dieta_pk')
        dieta = Dieta.objects.get(pk=pk)
        return dieta

    def get_success_url(self):
        dieta = self.get_object()
        my_user = dieta.my_user
        messages.success(self.request, 'Modifiche salvate con successo!')
        return reverse_lazy("Diet:mostradietauser", kwargs={"pk": my_user.pk})


# ------------------------------------------------------------------ #
# View per la creazione di un giorno
# ------------------------------------------------------------------ #
class GiornoDietaCreateView(CreateView):
    template_name = "Diet/crea_giorno.html"
    form_class = InsertGiornoForm

    def get_dieta(self):
        dieta_pk = self.kwargs.get('dieta_pk')
        dieta = Dieta.objects.get(pk=dieta_pk)
        return dieta

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dieta = self.get_dieta()
        context['dieta'] = dieta
        return context

    def form_valid(self, form):
        form.instance.dieta = self.get_dieta()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("Diet:crea_dettaglio", kwargs={"giorno_pk": self.object.pk})


class GiornoDietaDeleteView(DeleteView):
    model = GiornoDieta
    template_name = "Diet/delete_giorno.html"

    def get_object(self, queryset=None):
        giorno_pk = self.kwargs.get('giorno_pk')
        giorno = GiornoDieta.objects.get(pk=giorno_pk)
        return giorno

    def get_user(self):
        giorno = self.get_object()
        pk_user = giorno.dieta.my_user.pk
        return pk_user

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        giorno_pk = self.kwargs.get('giorno_pk')
        giorno = GiornoDieta.objects.get(pk=giorno_pk)
        context['gionro'] = giorno
        context['my_user'] = giorno.dieta.my_user
        return context

    def get_success_url(self):
        pk_user = self.get_user()
        return reverse("Diet:mostradietauser", kwargs={"pk": pk_user})



# ------------------------------------------------------------------ #
# View per creare un dettaglio di un giorno e un alimento
# ------------------------------------------------------------------ #
class DettaglioGiornoAlimentoCreateView(CreateView):
    template_name = "Diet/crea_dettaglio.html"
    form_class = FormDettaglioGiornoAlimento

    def get_giorno(self):
        pk_giorno = self.kwargs.get('giorno_pk')
        giorno = GiornoDieta.objects.get(pk=pk_giorno)
        return giorno

    def form_valid(self, form):
        form.instance.giorno = self.get_giorno()
        return super().form_valid(form)

    def get_success_url(self):

        # Recupero gli oggetti che mi servono dal form appena creato
        alimento = self.object.alimento
        quantita = self.object.quantita
        giorno = self.get_giorno()

        macro = alimento.get_macro_float()
        macro_pesati = tuple((x*quantita)/100 for x in macro)
        giorno.update_macro(macro_pesati)

        # Ritorno al mostra_giorni di una dieta
        return reverse_lazy("Diet:mostradietauser", kwargs={'pk': giorno.dieta.my_user.pk})


# --------------------------------------------------------------------------- #
# View che modifica la quantita di un alimento in un giorno, se la modifica
# va a buon fine ritorno alla visualizzazione della dieta completa dell'utente
# --------------------------------------------------------------------------- #
class DettaglioDietaAlimentoEditView(UpdateView):
    model = DettaglioGiornoAlimento
    form_class = DettaglioDietaUpdateForm
    template_name = 'Diet/modifica_dettaglio.html'

    def get_object(self, queryset=None):
        dettaglio_pk = self.kwargs.get('dettaglio_pk')
        dettaglio = DettaglioGiornoAlimento.objects.get(pk=dettaglio_pk)
        return dettaglio

    def get_success_url(self):
        dettaglio = self.get_object()

        # TODO update macro con la nuva quantita
        user_pk = dettaglio.giorno.dieta.my_user.pk
        return reverse_lazy("Diet:mostradietauser", kwargs={'pk': user_pk})

        #return reverse_lazy("Diet:mostra_giorni", kwargs={'dieta_pk':giorno.dieta.pk})








# ------------------------------------------------------------------ #
# View mostra la dieta completa di un utente dalla pk dell'utente
# ------------------------------------------------------------------ #
class MostraDietaUser(DetailView):
    model = Dieta
    template_name = "Diet/mostradietautente.html"
    context_object_name = "dieta"  # Nome dell'oggetto nel template

    # Metodo che utilizzo per recuperare l'user dalla pk nell'url
    def get_user(self):
        pk = self.kwargs.get('pk')
        my_user = MyUser.objects.get(pk=pk)
        return my_user

    # Metodo che utilizzo per recuperare la dieta dall'user
    def get_object(self, queryset=None):

        try:
            user = self.get_user()
            dieta = Dieta.objects.filter(my_user=user).latest('pk')
            return dieta

        except Dieta.DoesNotExist:
            print("la dieta non esiste")
            print(Exception)

    # Metodo che utilizzo per creare altri dati di contesto da mostrare nel
    # template come il dettaglio di una dieta diviso in giorni e pasti
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        dieta = self.get_object()
        dett = []

        giorni_dieta = GiornoDieta.objects.filter(dieta=dieta)
        for giorno_dieta in giorni_dieta:
            dettagli = DettaglioGiornoAlimento.objects.filter(giorno=giorno_dieta)
            dett.extend(dettagli)
        context['dettagli'] = dett
        context['giorni_dieta'] = giorni_dieta
        context['my_user'] = self.get_user()
        context['dieta'] = dieta
        return context












# ------------------------------------------------------------------ #
# Metodo che utilizzo per mostrare i giorni già creati di una dieta
# data la primary key della dieta
# ------------------------------------------------------------------ #
def mostra_giorni(request, dieta_pk):
    dieta = Dieta.objects.get(pk=dieta_pk)
    giorni = GiornoDieta.objects.all().filter(dieta=dieta)
    context = {
        'dieta': dieta,
        'giorni': giorni
    }
    return render(request, template_name="Diet/listagiorni.html", context=context)



# ------------------------------------------------------------------ #
# View mostra la dieta completa di un utente dalla pk dell'utente
# ------------------------------------------------------------------ #
class MostraDietaUser(DetailView):
    model = Dieta
    template_name = "Diet/mostradietautente.html"
    context_object_name = "dieta"  # Nome dell'oggetto nel template

    # Metodo che utilizzo per recuperare l'user dalla pk nell'url
    def get_user(self):
        pk = self.kwargs.get('pk')
        my_user = MyUser.objects.get(pk=pk)
        return my_user

    # Metodo che utilizzo per recuperare la dieta dall'user
    def get_object(self, queryset=None):

        try:
            user = self.get_user()
            dieta = Dieta.objects.filter(my_user=user).latest('pk')
            return dieta

        except Dieta.DoesNotExist:
            print("la dieta non esiste")
            print(Exception)

    # Metodo che utilizzo per creare altri dati di contesto da mostrare nel
    # template come il dettaglio di una dieta diviso in giorni e pasti
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        dieta = self.get_object()
        dett = []

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
class DettaglioDietaCreateView(CreateView):
    template_name = 'Diet/crea_dettaglio.html'
    form_class = InsertDettaglioDietaCrispyForm

    # Metodo per ottenere l'alimento
    def get_alimento(self):
        try:
            alimento_pk = self.kwargs.get('alimento_pk')
            alimento = Alimento.objects.get(pk=alimento_pk)
            return alimento
        except Alimento.DoesNotExist:
            print("alimento non esiste")
            return None

    # Metodo per ottenere la dieta
    def get_dieta(self):
        try:
            dieta_pk = self.kwargs.get('dieta_pk')
            dieta = Dieta.objects.get(pk=dieta_pk)
            return dieta
        except Dieta.DoesNotExist:
            print("dieta non esiste")
            return None

    # Metodo che utilizzo per impostare la dieta e l'alimento
    # di cui voglio inserire la quantita all'interno del DB
    def form_valid(self, form):
        form.instance.dieta = self.get_dieta()
        form.instance.alimento = self.get_alimento()
        return super().form_valid(form)

    # Dopo aver inserito un dettaglio-dieta
    def get_success_url(self):
        return reverse_lazy("Diet:mostra_dettaglio", kwargs={"pk": self.kwargs.get('dieta_pk')})
# --------------------------------------------------------------------------------------------------- #
"""

# --------------------------------------------------------------------------------------------------- #
def mostra_dettaglio_dieta(request, pk):
    dieta = Dieta.objects.get(pk=pk)
    context = {
        'pk_dieta': pk,
        'alimenti': Alimento.objects.all(),
        'dieta': dieta
    }
    return render(request, template_name='Diet/lista_alimenti.html', context=context)
# --------------------------------------------------------------------------------------------------- #



