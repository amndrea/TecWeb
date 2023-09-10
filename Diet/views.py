from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from .models import *
from .forms import InsertAlimentoCrispyForm, InsertDietaCrispyForm, InsertDettaglioDietaCrispyForm


# Classe per inserire un alimento
# solo l'admin può inserire alimenti
class AlimentoCreateView(CreateView):
    template_name = 'Diet/crea_alimento.html'
    form_class = InsertAlimentoCrispyForm
    success_url = reverse_lazy("Diet:lista_alimenti")


# Classe per visualizzare la lista di alimenti
class AlimentoListView(ListView):
    model = Alimento
    template_name = "Diet/lista_alimenti.html"


# Classe per inserire una dieta
class DietaCreateView(CreateView):
    template_name = 'Diet/crea_dieta.html'
    form_class = InsertDietaCrispyForm

    # Dopo aver creato una dieta mi redireziono nella pagina per inserire gli alimenti
    def get_success_url(self):
        ctx = self.get_context_data()
        pk = ctx["object"].pk
        return reverse_lazy("Diet:mostra_dettaglio", kwargs={"pk": pk})


class DettaglioDietaCreateView(CreateView):
    template_name = 'Diet/crea_dettaglio.html'
    form_class = InsertDettaglioDietaCrispyForm

    def get_alimento(self):
        try:
            alimento_pk = self.kwargs.get('alimento_pk')
            alimento = Alimento.objects.get(pk=alimento_pk)
            return alimento
        except Alimento.DoesNotExist:
            print("alimento non esiste")
            return None

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

    # TODO IMPOSTARE UN CORRETTO URL
    def get_success_url(self):
        return reverse_lazy("Diet:crea_alimento")
# ------------------------------------------------------------------------#


def mostra_dettaglio_dieta(request, pk):
    """
    Metodo che utilizzo per visualizzare tutti gli alimenti da poter inserire in una dieta
    Per ogni alimento nel template c'è un pulsante seleziona che consente di selezionare
    l'alimento ed inserirlo nella dieta
    :param request:
    :param pk: primary key della dieta
    :return: render della pagina con tutti i possibili alimenti da inserire nella dieta
    """
    context = {
        'pk_dieta': pk,
        'alimenti': Alimento.objects.all()
    }
    return render(request, template_name='Diet/lista_alimenti.html', context=context)


# In questa view mostro i dettagli completi di una dieta data la sua primary key
class MostraDietaCompleta(DetailView):

    model = Dieta
    template_name = 'Diet/mostra_dieta.html'

    # Metodo che utilizzo per avere il riferimento all'oggetto dieta corrente
    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return self.model.objects.get(pk=pk)

    # Dalla dieta ottengo anche tutti i dettaglio_dieta con gli alimenti e le quantità
    # E li passo al context per visualizzarli nel template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dieta = self.get_object()  # Ottengo l'oggetto dieta corrente
        dettaglio_dieta = DettaglioDieta.objects.filter(dieta=dieta).order_by('giorni', 'pasto')
        context['dettaglio_dieta'] = dettaglio_dieta
        return context
