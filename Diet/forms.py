from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from .models import *


class InsertDietaCrispyForm(forms.ModelForm):
    """
    Classe che crea un form per l'inserimento di una dieta nel DB
    """
    helper = FormHelper()
    helper.form_id = "insert_dieta_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit('submit', 'submit'))


    class Meta:

        # Su quale modello sto andando a lavorare
        model = Dieta

        # Quali campi consento di editare
        exclude=['my_user']

class InsertGiornoForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "insert_giorno_form"
    helper.form_method = "POST"
    helper.add_input(Submit('Crea', 'Crea'))

    class Meta:
        model = GiornoDieta
        fields = ['giorno']

class InsertDettaglioDietaCrispyForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "insert_dettagliodieta_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit('submit', 'submit'))

    class Meta:
        model = DettaglioDieta
        fields = ['pasto', 'quantita']


