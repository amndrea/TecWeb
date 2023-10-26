from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from .models import *


class MessaggioCreateForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "invia_messaggio"
    helper.form_method = "POST"
    helper.add_input(Submit('submit', 'submit'))

    class Meta:
        model = Messaggio
        fields = ['testo']