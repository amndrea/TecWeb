from django.shortcuts import render
from Users.models import MyUser


# Funzione che mostra la home
def mostra_home(request):
    return render(request, template_name="home.html")


# Funzione che mostra la home di un utente loggato
def mostra_home_log(request):
    pk = request.user.pk
    context = {
        'user_pk': pk,
    }
    return render(request,template_name="home_login.html",context=context)
