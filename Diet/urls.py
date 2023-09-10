from django.urls import path
from Diet.views import *
from .initcmd import *

app_name = "Diet"

urlpatterns = [
    path('listaalimenti/', AlimentoListView.as_view(), name='lista_alimenti'),
    path('creaalimento/', AlimentoCreateView.as_view(), name='crea_alimento'),
    path('creadieta/', DietaCreateView.as_view(), name="crea_dieta"),
    path('mostradettaglio/<pk>/', mostra_dettaglio_dieta, name="mostra_dettaglio"),
    path('creadettaglio/<int:dieta_pk>/<int:alimento_pk>/', DettaglioDietaCreateView.as_view(), name="crea_dettaglio"),

    # URL al quale mostro tutti i dettagli di una dieta
    path('mostradieta/<pk>/', MostraDietaCompleta.as_view(), name="mostra_dieta")
]

#svuota_tabelle()
#salva_alimenti_su_file()
#carica_alimenti()

