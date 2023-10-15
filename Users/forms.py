from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

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
        exclude = ['fine_abbonamento', 'tipo_abbonamento', 'password', 'last_login', 'is_superuser', 'groups', 'user_permissions', 'is_staff', 'is_active', 'date_joined']

    # Metodo per aggiungere l'utente appena registrato al gruppo cliente
    def save(self, commit=True):
        user = super().save(commit)
        g = Group.objects.get(name="cliente")
        g.user_set.add(user)
        return user


class CreaNutrizionista(CreaUtenteCrispyForms):

    # Metodo per aggiungere un nutrizionista, eredita da CreaUtenteCrispyForms
    # e modifica il gruppo in nutrizionista
    def save(self, commit=True):
        user = super().save(commit)
        user.tipo_abbonamento = 1
        g = Group.objects.get(name="nutrizionista")
        g.user_set.add(user)
        return user


class CreaPersonalTrainer(CreaUtenteCrispyForms):
    def save(self, commit=True):
        user = super().save(commit)
        g = Group.objects.get(name="pt")
        g.user_set.add(user)
        return user


# --------------------------------------------------------------------------------------- #
# Form per l'update dell'utente
# --------------------------------------------------------------------------------------- #
class UtenteUpdateform(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "edit_user_form"
    helper.form_method = "POST"
    helper.add_input(Submit('submit', 'submit'))

    class Meta:
        model = MyUser
        fine_abbonamento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
        fields = ['altezza', 'peso', 'fine_abbonamento', 'tipo_abbonamento']


class UtenteUpdatePeso(UtenteUpdateform):
    class Meta:
        model = MyUser
        fields = ['peso']


class UtenteUpdateAltezza(UtenteUpdateform):
    class Meta:
        model = MyUser
        fields = ['altezza']


class UtenteUpdateFoto(UtenteUpdateform):
    class Meta:
        model = MyUser
        fields = ['immagine_profilo']
# --------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------- #
