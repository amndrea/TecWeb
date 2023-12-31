"""
URL configuration for GestionalePalestra project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import mostra_home, mostra_home_log
from django.conf import settings
from django.conf.urls.static import static
from .initcmd import crea_gruppi

urlpatterns = [
    path('admin/', admin.site.urls),
    path("workout/", include("Workout.urls")),
    path("diet/", include("Diet.urls")),
    path("user/", include("Users.urls")),
    path("prenotazioni/",include("Prenotazioni.urls")),
    path("chat/",include("Chat.urls")),

    # LOGIN E LOGOUT
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    # URL ai quali mostro la schermata home
    path("", mostra_home, name="home"),

    # URL al quale mostro la home dell'utente loggato
    path("home_login/", mostra_home_log, name="home_login")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# crea_gruppi()