from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import InsertSchedaCrispyForm
from .models import Esercizio


# --------------------------------------------------------------------------------------------------- #
#     Classe che utilizzo per creare una schesa, solo i PT possono creare una scheda
# --------------------------------------------------------------------------------------------------- #
class SchedaCreateView(CreateView):
    template_name = "Workout/crea_scheda.html"
    form_class = InsertSchedaCrispyForm

    def get_success_url(self):
        ctx = self.get_context_data()
        pk = ctx["object"].pk
        return reverse_lazy("Workout:creascheda")


class DettaglioCreateView(CreateView):
    pass


def listaesercizi(request, pk):

    context = {
        'pk_scheda': pk,
        'esercizi': Esercizio.objects.all()
    }
    return render(request, template_name='Workout/lista_esercizi.html',context=context)
