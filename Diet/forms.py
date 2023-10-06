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

class DietaUpdateForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "edit_dieta_form"
    helper.form_method = "POST"
    helper.add_input(Submit('submit', 'submit'))

    data_inizio = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),required=False)
    data_fine = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Dieta
        fields = ['tipologia', 'descrizione', 'data_inizio', 'data_fine']
    tipologia = forms.CharField(required=False)
    descrizione = forms.CharField(required=False)

    #data_inizio = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),required=False)
    #data_fine = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),required=False)

class InsertGiornoForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "insert_giorno_form"
    helper.form_method = "POST"
    helper.add_input(Submit('Crea', 'Crea'))

    class Meta:
        model = GiornoDieta
        fields = ['giorno']


class FormDettaglioGiornoAlimento(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "insert_giorno_form"
    helper.form_method = "POST"
    helper.add_input(Submit('Crea', 'Crea'))

    class Meta:
        model = DettaglioGiornoAlimento
        exclude = ['giorno']


class DettaglioDietaUpdateForm(forms.ModelForm):
    class Meta:
        model = DettaglioGiornoAlimento
        fields = ['quantita']












"""
class InsertDettaglioDietaCrispyForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "insert_dettagliodieta_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit('submit', 'submit'))

    class Meta:
        model = DettaglioDieta
        fields = ['pasto', 'quantita']


class DietaUpdateForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "edit_dieta_form"
    helper.form_method = "POST"
    helper.add_input(Submit('submit', 'submit'))

    data_inizio = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),required=False)
    data_fine = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Dieta
        fields = ['tipologia', 'descrizione', 'data_inizio', 'data_fine']
    tipologia = forms.CharField(required=False)
    descrizione = forms.CharField(required=False)

    #data_inizio = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),required=False)
    #data_fine = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),required=False)
"""