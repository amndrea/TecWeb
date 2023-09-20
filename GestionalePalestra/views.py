from django.shortcuts import render

# Funzione che mostra la home
def mostra_home(request):
    return render(request, template_name="home.html")

