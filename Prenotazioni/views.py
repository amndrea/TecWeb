from django.shortcuts import render


# View per mostrare una pagina HTML contenente un calendario
def mostra_calendario(request):
    parametri = request.GET
    if 'year' in parametri and 'month' in parametri:
        anno = int(parametri['year'])
        mese = int(parametri['month'])
        print(anno)
        print(mese)

    return render(request,"Prenotazioni/calendario.html")
