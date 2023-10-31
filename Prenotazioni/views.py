from django.http import HttpResponseRedirect
from django.shortcuts import render
import datetime

from django.urls import  reverse

from Users.models import MyUser
from .models import *
from django.core.exceptions import ObjectDoesNotExist

# View per mostrare una pagina HTML contenente un calendario
def mostra_calendario(request, user_pk):
    parametri = request.GET
    if 'year' in parametri and 'month' in parametri:
        anno = int(parametri['year'])
        mese = int(parametri['month'])
        print(anno)
        print(mese)

    return render(request,"Prenotazioni/calendario.html")



# View per mostrare i giorni e permettere il
# prenotamento di un orario
def mostra_giorno(request, year, month, day):
    data = datetime.date(year,month,day)
    ctx = {}
    # Domenica la palestra è chiusa tutto il giorno
    domenica = 1 if data.weekday() == 6 else 0
    prenotazione = None

    if not domenica:
        try:
            giorno_i = Giorno.objects.get(anno=year, mese=month, giorno=day)
        except ObjectDoesNotExist:
            giorno_i, creato = Giorno.objects.get_or_create(anno=year, mese=month, giorno=day)
        ctx["giorno"] = giorno_i
        prenotazione = datetime.date(giorno_i.anno, giorno_i.mese, giorno_i.giorno)

    ctx["domenica"] = domenica
    oggi = datetime.date.today()

    if prenotazione is not None and prenotazione < oggi and not domenica:
        return render(request, "Prenotazioni/errore.html")
    else:
        orari = ["8:00","9:00","10:00","11:00","12:00","13:00","14:00","15:00","16:00","17:00","18:00","19:00","20:00"]
        ctx['orari'] = orari
        return render(request, "Prenotazioni/giorno.html",ctx)




def effettua_prenotazione(request, orario, giorno_pk, utente_pk):
    ctx = {}
    # Conversione da orario in formato stringa a intero
    i = orario.find(":")
    orario = orario[0:i]
    orario = int(orario)


    # Controllo che l'utente abbia l'abbonamento valido, se non è valido mando alla sezione personale
    my_user = MyUser.objects.get(pk=utente_pk)
    oggi = datetime.date.today()

    if my_user.fine_abbonamento < oggi:
        return HttpResponseRedirect(reverse('Users:situazione', args=[my_user.pk]))


    # Controllo che la prenotazione dell'utente non ci sia gia in quel giorno e in quell'ora
    # Se non c'è la inserisco e la
    giorno = Giorno.objects.get(pk=giorno_pk)
    prenotazioni = Prenotazione.objects.filter(giorno=giorno).filter(ora=orario)

    i = 0
    for prenotazione in prenotazioni:
        i=i+1

    # Se sono a capienza massima
    if i >= 3:
        ctx['pieno'] = True
        # Controllo di non aver gia effettuato la prenotazione, per il context
        try:
            prenotazione = Prenotazione.objects.get(giorno=giorno, user=my_user, ora=orario)
            ctx['gia_prenotato'] = True
        except ObjectDoesNotExist:
            pass
    # Altrimenti tento di inserire una prenotazione
    else:
        try:
            prenotazione = Prenotazione.objects.get(giorno=giorno, user=my_user, ora=orario)
            print("prenotazione gia effettuata")
            ctx['gia_prenotato'] = True

        # Se l'oggetto non esiste, lo creo
        except ObjectDoesNotExist:
            ctx['gia_prenotato'] = False
            prenotazione = Prenotazione()
            prenotazione.giorno = giorno
            prenotazione.user = my_user
            prenotazione.ora = orario
            prenotazione.save()

    prenotazioni = Prenotazione.objects.filter(giorno=giorno).filter(ora=orario)
    ctx['prenotazioni'] = prenotazioni
    ctx['giorno'] = giorno
    ctx['ora'] = orario
    return render(request, "Prenotazioni/prenota.html", ctx)
