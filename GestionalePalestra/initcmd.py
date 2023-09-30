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

    lista_permessi = ['add_dieta', 'add_dettagliodieta', 'change_dieta', 'change_dettagliodieta', 'delete_dieta',
                      'delete_dettagliodieta']
    for perm in lista_permessi:
        permesso = Permission.objects.get(codename=perm)
        nutrizionista.permissions.add(permesso)
