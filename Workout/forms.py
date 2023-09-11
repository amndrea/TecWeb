import form as form
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from .models import Scheda


# Form per inserire i campi di una scheda
class InsertSchedaCrispyForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "insert_scheda_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit('submit', 'submit'))

    class Meta:
        model = Scheda
        fields = '__all__'

