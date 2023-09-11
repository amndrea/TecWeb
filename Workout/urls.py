from django.urls import path
from .views import *

app_name = "Workout"

urlpatterns = [

    #URL per creare una scheda
    path('creascheda/',SchedaCreateView.as_view(),name="creascheda"),


]

# DeleteEsercizio
# RiempiDbEsercizio
