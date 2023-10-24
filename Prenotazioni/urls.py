from django.urls import path
from .views import *

app_name = "Prenotazioni"

urlpatterns = [
    path("mostra_calendario/",mostra_calendario,name="calendario"),
    path("calendario/<int:anno>/<int:mese>",mostra_calendario,name="calendario"),

]
