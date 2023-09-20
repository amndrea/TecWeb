from django.urls import path
from .views import *

app_name = "Users"

urlpatterns = [
    # URL al quale un utente tenta la registrazione
    path('creautente/', UserCreateView.as_view(), name="crea_utente"),
]
