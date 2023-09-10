from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from .models import *


class InsertAlimentoCrispyForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "insert_alimento_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit('submit', 'submit'))

    # Metodo che controlla la correttezza dei dati inseriti
    def clean(self):
        if self.cleaned_data["proteine"] < 0:
            self.add_error("Proteine", "Le proteine devono essere presenti ")
        if self.cleaned_data["carboidrati"] < 0:
            self.add_error("Carboidrati", "I carboidrati devono essere presenti ")
        if self.cleaned_data["grassi"] < 0:
            self.add_error("Grassi", "I grassi devono essere presenti ")
        if self.cleaned_data["kcal"] < 0:
            self.add_error("Kcal", "Le Kcal devono essere presenti ")

        return self.cleaned_data

    class Meta:
        model = Alimento
        fields = "__all__"


class InsertDietaCrispyForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "insert_dieta_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit('submit', 'submit'))

    class Meta:
        model = Dieta
        fields = '__all__'


class InsertDettaglioDietaCrispyForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "insert_dettagliodieta_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit('submit', 'submit'))

    class Meta:
        model = DettaglioDieta
        fields = ['giorni', 'pasto', 'quantita']

