#import form as form
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from .models import *


# Form per l'inserimento di una scheda
class SchedaCreateForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "scheda_create_form"
    helper.form_method = "POST"
    helper.add_input(Submit('submit', 'submit'))

    data_inizio = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    data_fine = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),required=False)

    class Meta:
        model = Scheda
        exclude = ['my_user']

class GiornoCreateForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "scheda_create_form"
    helper.form_method = "POST"
    helper.add_input(Submit('submit', 'submit'))

    class Meta:
        model = GiornoScheda
        exclude = ['Scheda']

class DettaglioGiornoEsercizioForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "dettaglio_create_form"
    helper.form_method = "POST"
    helper.add_input(Submit('submit', 'submit'))

    class Meta:
        model = DettaglioEsercizioGiorno
        exclude = ['giorno']



# ------------------------------------------------------------------------------- #
#  Form per la modifica di un dettaglio Esercizio - Giorno
# ------------------------------------------------------------------------------- #
class DettagliGiornoEsercizioForm (forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "dettaglio_create_form"
    helper.form_method = "POST"
    helper.add_input(Submit('submit', 'submit'))


    class Meta:
        model = DettaglioEsercizioGiorno
        fields = '__all__'

class DettaglioUpdateSerie(DettagliGiornoEsercizioForm):
    class Meta:
        model = DettaglioEsercizioGiorno
        fields = ['serie']

class DettaglioUpdateRipetizioni(DettagliGiornoEsercizioForm):
    class Meta:
        model = DettaglioEsercizioGiorno
        fields = ['ripetizioni']

class DettaglioUpdateRecupero(DettagliGiornoEsercizioForm):
    class Meta:
        model = DettaglioEsercizioGiorno
        fields = ['recupero']

