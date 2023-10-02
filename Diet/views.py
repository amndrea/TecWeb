from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from .models import *
from Users.models import MyUser
from .forms import InsertDietaCrispyForm, InsertDettaglioDietaCrispyForm


# --------------------------------------------------------------------------------------------------- #
class DietaCreateView(CreateView):
    """
    Classe che utilizzo per creare una dieta, solo i PR possono creare una dieta
    """
    template_name = 'Diet/crea_dieta.html'
    form_class = InsertDietaCrispyForm

    def get_user(self):
        user_pk = self.kwargs.get('utente_pk')
        try:
            user = MyUser.objects.get(pk=user_pk)
            return user
        except Exception:
            print("qualcosa è andato male")

    def form_valid(self, form):
        form.instance.my_user = self.get_user()
        return super().form_valid(form)


    # Dopo aver creato una dieta mi redireziono nella pagina per inserire gli alimenti
    def get_success_url(self):
        ctx = self.get_context_data()
        pk = ctx["object"].pk
        print("sono la chiave")
        print(pk)
        return reverse_lazy("Diet:mostra_dettaglio", kwargs={"pk": pk})
# --------------------------------------------------------------------------------------------------- #

def show_dettaglio(request):
    pass
# --------------------------------------------------------------------------------------------------- #
class DettaglioDietaCreateView(CreateView):
    """
    Classe che utilizzo per Inserire un dettaglio in una dieta
    Dato un Alimento e data una dieta Inserisco i vari campi del Dettaglio
    """
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


# --------------------------------------------------------------------------------------------------- #
def mostra_dettaglio_dieta(request, pk):
    """
    Metodo che utilizzo per visualizzare tutti gli alimenti da poter inserire in una dieta
    Per ogni alimento nel template c'è un pulsante seleziona che consente di selezionare
    l'alimento e inserirlo nella dieta
    :param request:
    :param pk: primary key della dieta
    :return: render della pagina con tutti i possibili alimenti da inserire nella dieta
    """
    dieta = Dieta.objects.get(pk=pk)
    context = {
        'pk_dieta': pk,
        'alimenti': Alimento.objects.all(),
        'dieta': dieta
    }
    return render(request, template_name='Diet/lista_alimenti.html', context=context)
# --------------------------------------------------------------------------------------------------- #


# --------------------------------------------------------------------------------------------------- #
class MostraDietaCompleta(DetailView):
    """
    Classe per visualizzare i dettagli completi di una dieta data la primary key della dieta
    """

    model = Dieta
    template_name = 'Diet/mostra_alimenti.html'

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
# --------------------------------------------------------------------------------------------------- #


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

        try:
            dettaglio_dieta = DettaglioDieta.objects.filter(dieta=dieta).order_by('giorni')
            context['dettaglio_dieta'] = dettaglio_dieta
            colazioni = dettaglio_dieta.filter(pasto="coalzione")
            context['colazioni'] = colazioni
            spuntini = dettaglio_dieta.filter(pasto="spuntino")
            context['spuntini'] = spuntini
            pranzi = dettaglio_dieta.filter(pasto="pranzo")
            context['pranzi'] = pranzi
            merende = dettaglio_dieta.filter(pasto="merenda")
            context['merende'] = merende
            cene = dettaglio_dieta.filter(pasto="cena")
            context['cene'] = cene

        except Exception:
            context['dettaglio_dieta'] = None

        context['dieta'] = dieta
        return context
