from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CreaUtenteCrispyForms
from django.contrib.auth.mixins import PermissionRequiredMixin
from braces.views import GroupRequiredMixin
from django.contrib.auth.forms import UserCreationForm
import datetime

# Classe che implementa la creazione di un utente grazie alla classe CreaUtenteCrispyForms
class UserCreateView(CreateView):
    form_class = CreaUtenteCrispyForms
    template_name = "Users/crea_utente.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        form.instance.fine_abbonamento = datetime.date.today()
        form.instance.tipo_abbonamento = 0
        return super().form_valid(form)
