from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CreaUtenteCrispyForms


# Classe che implementa la creazione di un utente grazie alla classe CreaUtenteCrispyForms
class UserCreateView(CreateView):
    form_class = CreaUtenteCrispyForms
    template_name = "Users/crea_utente.html"
    success_url = reverse_lazy("login")
