import form as form
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from .models import *


# Form per l'inserimento di una scheda
class SchedaCreateForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "edit_dieta_form"
    helper.form_method = "POST"
    helper.add_input(Submit('submit', 'submit'))

    data_inizio = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    data_fine = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),required=False)

    class Meta:
        model = Scheda
        exclude = ['my_user']
