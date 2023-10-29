from django.urls import path
from .views import *

app_name = "Prenotazioni"

urlpatterns = [

    path("mostra_calendario/",mostra_calendario,name="calendario"),

]
