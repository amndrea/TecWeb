from django.shortcuts import render, redirect
import datetime
from .models import *
from django.core.exceptions import ObjectDoesNotExist

# View per mostrare una pagina HTML contenente un calendario
def mostra_calendario(request):
    parametri = request.GET
    if 'year' in parametri and 'month' in parametri:
        anno = int(parametri['year'])
        mese = int(parametri['month'])
        print(anno)
        print(mese)

    return render(request,"Prenotazioni/calendario.html")



# View per mostrare i giorni e permettere il prenotamento di un orario
def mostra_giorno(request, year, month, day):
    data = datetime.date(year,month,day)
    ctx = {}
    # Domenica la palestra è chiusa tutto il giorno
    domenica = 1 if data.weekday() == 6 else 0

    if not domenica:
        try:
            giorno_i = Giorno.objects.get(anno=year,mese=month,giorno=day)
        except ObjectDoesNotExist:
            giorno_i, creato = Giorno.objects.get_or_create(anno=year, mese=month, giorno=day)
        ctx["giorno"] = giorno_i

    ctx["doemnica"] = domenica
    oggi = datetime.date.today()

    if giorno_i.anno == oggi.year and giorno_i.mese == oggi.month:
        if giorno_i.giorno < oggi.day:
            pass
    # Controllo che il giorno della prenotazione sia possibile
    if giorno_i.anno < oggi.year:
        ctx['errore'] = True
    else:

        print("si")
    return render(request,'Prenotazioni/giorno.html',ctx)