from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import MyUser


# Classe che usa un utente non registrato per effettuare la registrazione all'app
class CreaUtenteCrispyForms(UserCreationForm):
    helper = FormHelper()
    helper.form_id = "crea_utente_form"
    helper.form_method = "POST"
    helper.add_input(Submit('submit', 'submit'))

    class Meta:

        # Vado a creare un'entità nel modello MyUser
        model = MyUser

        # Non lascio editare tutti i campi, escludo quelli che non possono
        # Essere creati direttamente dall'utente ma devono essere editati dal PT
        # o da un dipendente della palestra dopo il pagamento dell'abbonamento
        # e tutti quei campi che non voglio lasciar editare come i permessi
        exclude =['fine_abbonamento','tipo_abbonamento','password','last_login','is_superuser','groups','user_permissions','is_staff','is_active','date_joined']
