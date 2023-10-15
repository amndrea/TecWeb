from django.contrib.auth.models import Group, Permission


# ------------------------------------------------------------ #
#                    Creazione di gruppi
# ------------------------------------------------------------ #
def crea_gruppi():
    cliente, creato_ciente = Group.objects.get_or_create(name="cliente")
    personal_trainer,creato_pt = Group.objects.get_or_create(name="pt")

    # Permessi del nutrizionista
    nutrizionista, creato_n = Group.objects.get_or_create(name="nutrizionista")
    if creato_n or creato_pt or creato_ciente:
        print("creati i gruppi")
    else:
        print("gruppi gia esistenti")

    lista_permessi_nutrizionista = ['add_dieta','change_dieta','delete_dieta','view_dieta',
                      'add_giornodieta','change_giornodieta','delete_giornodieta','view_giornodieta',
                      'add_dettagliogiornoalimento','change_dettagliogiornoalimento','delete_dettagliogiornoalimento','view_dettagliogiornoalimento',
    ]

    lista_permessi_pt = [ 'add_scheda', 'change_scheda','delete_scheda','view_scheda'

    ]

    for perm in lista_permessi_nutrizionista:
        try:
            permesso = Permission.objects.get(codename=perm)
        except Permission.DoesNotExist:
            permesso = Permission.objects.create(codename=perm)
        nutrizionista.permissions.add(permesso)


    for perm in lista_permessi_pt:
        try:
            permesso = Permission.objects.get(codename=perm)
        except Permission.DoesNotExist:
            permesso = Permission.objects.create(codename=perm)
        personal_trainer.permissions.add(permesso)
