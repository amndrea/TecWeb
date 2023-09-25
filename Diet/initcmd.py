from .models import *
import os
import pickle

def svuota_tabelle():
    print("Elimino tutte le entità nel database")
    Alimento.objects.all().delete()
    Dieta.objects.all().delete()
    DettaglioDieta.objects.all().delete()


def salva_alimenti_su_file():
    directory = os.getcwd()
    file_path = str(directory) + "\\static\\data\\alimenti.txt"

    alimenti = Alimento.objects.all()
    try:
        with open(file_path, 'w') as file:
            for alimento in alimenti:
                file.write(str(alimento.nome) + "\n")
                file.write(str(alimento.proteine) + "\n")
                file.write(str(alimento.carboidrati) + "\n")
                file.write(str(alimento.grassi) + "\n")
                file.write(str(alimento.cal) + "\n")

    except FileNotFoundError:
        print("file non trovato")


def carica_alimenti():
    directory = os.getcwd()
    file_path = str(directory) + "\\static\\data\\alimenti.txt"

    try:
        with open(file_path, 'r') as file:
            righe = file.readlines()
            for i in range(0, len(righe), 5):
                dati_alimento = righe[i:i + 5]

                a = Alimento()
                a.nome = dati_alimento[0].strip()
                a.proteine = dati_alimento[1].strip()
                a.carboidrati = dati_alimento[2].strip()
                a.grassi = dati_alimento[3].strip()
                a.cal = dati_alimento[4].strip()

                try:
                    a.save()
                except Exception:
                    print("alimento gia presente nel db")

    except FileNotFoundError:
        print("Non trovato il file per il caricamento dei dati")
