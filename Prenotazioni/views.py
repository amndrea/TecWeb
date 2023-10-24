from django.shortcuts import render
import calendar
from calendar import HTMLCalendar
# Create your views here.
def mostra_calendario(request):
    return render(request,"Prenotazioni/calendario.html")

