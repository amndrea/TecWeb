import datetime

from django.test import TestCase
from django.urls import reverse
from .models import Giorno, Prenotazione
from Users.models import MyUser
from datetime import date


class PrenotazioniTestCase(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(username='testuser', password='testpassword')
        self.user2 = MyUser.objects.create_user(username="user2", password="testpassword")
        self.user3 = MyUser.objects.create_user(username="user3", password="testpassword")
        self.user4 = MyUser.objects.create_user(username="user4", password="testpassword")



    def test_mostra_calendario(self):
        response = self.client.get('Prenotazioni:calendario',args=[self.user.pk])
        self.assertTemplateUsed("Prenotazioni:calendario.html")

    def test_prenota_domenica(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("Prenotazioni:mostra_giorno",args=[2023,11,5]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Prenotazioni/giorno.html')

        # Verifico che il giorno non venga creato visto che si parla di una domencia
        with self.assertRaises(Giorno.DoesNotExist):
            Giorno.objects.get(anno=2023, mese=11, giorno=5)

    def test_prenota_ok(self):
        self.client.force_login(self.user)
        oggi = datetime.date.today()
        data_fine_abbonamento = oggi + datetime.timedelta(days=1)
        self.user.fine_abbonamento = data_fine_abbonamento
        self.user.save()
        # creo un giorno possibile
        giorno = Giorno()
        giorno.anno = 2023
        giorno.mese=11
        giorno.giorno = 6
        giorno.save()
        orario = "9:00"
        response = self.client.get(reverse("Prenotazioni:prenota",args=[orario, giorno.pk, self.user.pk]))

        self.assertEqual(Prenotazione.objects.count(),1)

    def test_abbonamento_scaduto(self):
        self.client.force_login(self.user)
        oggi = datetime.date.today()
        # abbonamento scaduto
        data_fine_abbonamento = oggi + datetime.timedelta(days=-1)
        self.user.fine_abbonamento = data_fine_abbonamento
        self.user.save()
        # creo un giorno possibile
        giorno = Giorno()
        giorno.anno = 2023
        giorno.mese = 11
        giorno.giorno = 6
        giorno.save()
        orario = "9:00"
        response = self.client.get(reverse("Prenotazioni:prenota", args=[orario, giorno.pk, self.user.pk]))

        self.assertEqual(Prenotazione.objects.count(),0)


    def test_capienza_finita(self):
        self.client.force_login(self.user)
        oggi = datetime.date.today()
        data_fine_abbonamento = oggi + datetime.timedelta(days=1)
        self.user.fine_abbonamento = data_fine_abbonamento
        self.user.save()
        giorno = Giorno()
        giorno.anno = 2023
        giorno.mese = 11
        giorno.giorno = 7
        giorno.save()
        orario = "9:00"
        print("sono qua")
        print(giorno.pk)
        response = self.client.get(reverse("Prenotazioni:prenota", args=[orario, giorno.pk, self.user.pk]))
        self.client.logout()
        self.client.force_login(self.user2)
        self.user2.fine_abbonamento = data_fine_abbonamento
        self.user2.save()
        response = self.client.get(reverse("Prenotazioni:prenota",args=[orario, giorno.pk, self.user2.pk]))
        self.client.logout()
        self.client.force_login(self.user3)
        self.user3.fine_abbonamento = data_fine_abbonamento
        self.user3.save()
        response = self.client.get(reverse("Prenotazioni:prenota", args=[orario, giorno.pk, self.user3.pk]))

        # Ora ci prova un altro utente e non può prenotare
        self.client.logout()
        self.client.force_login(self.user4)
        self.user4.fine_abbonamento = data_fine_abbonamento
        self.user4.save()
        response = self.client.get(reverse("Prenotazioni:prenota", args=[orario, giorno.pk, self.user4.pk]))
        self.assertEqual(Prenotazione.objects.count(),3)
