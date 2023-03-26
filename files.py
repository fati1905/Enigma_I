# Le fichier "files.py" est responsable de la lecture des fichiers.
# Il lit l'entête du message qui est écrite sous la forme :
# Temps Actuel = Total des parties existantes = La partie actuelle = nombre de caractères = GRUNDSTELLUNG  Spruchschlussel chiffré
# Il lit ensuite les messages dans le fichier : KENNGRUPPEN Message séparé par des espaces toutes les 5 lettres

# Les variables représentant l'entête du fichier

time = None
nb_part = None
part = None
nb_car = None
key1 = None
kengruppen = None
message = []


def ReadFile(fichier):
    # Global variables
    global time, nb_part, part, nb_car, key1, kengruppen, message

    # Les variables booléens
    text_start = False      # Permet de savoir le début du texte
    heading = False         # Permet de savoir la ligne juste après l'entête pour récupérer le KENGRUPPEN

    # À chaque fois, on ouvre un fichier, on supprime l'ancien contenu de la liste des messages
    message.clear()
    ligne = fichier.readline()

    while True:
        # Tester s'il y a un '=' dans la ligne, si c'est le cas, on est dans un entête
        if "=" in ligne:
            #   Nous décomposons la ligne selon les '='
            ligne = ligne.split("=")

            # On récupère l'entête
            if len(ligne) == 5:
                time = ligne[0]
                nb_part = ligne[1]
                part = ligne[2]
                nb_car = ligne[3]
                key1 = ligne[4]

                heading = True  # On a rencontré un entête, donc la prochaine ligne contient le message avec le kengruppen
            else:
                print("L'entête n'est pas sous une bonne format :")
                print("heure = nombres de parties = nombre de la partie = nombres de caractères = la clé initiale\n")

        else:

            # Nous allons récupérer le kingruppen puisque c'est la première ligne après l'entête
            # Si heading est vrai et la ligne n'est pas vide, c'est effectivement la première ligne des messages
            if heading and ligne != "\n":  # Récupérer le kengruppen
                heading = False
                ligneList = ligne.split()
                # On récupère le kengruppen
                kengruppen = ligneList[0]
                # Puis, on le supprime pour ne pas le déchiffrer / chiffrer
                del ligneList[0]
                # La ligne du message sans le kengruppen
                ligne = " ".join([str(elem) for elem in ligneList])
                # Booléen montrant qu'on peut récupérer le texte
                text_start = True

            if text_start:
                # c'est un message
                message.append(ligne)

        # Lire la prochaine ligne
        ligne = fichier.readline()

        # Si c'est la fin du fichier, nous arrêtons la boucle
        if not ligne:
            break


#   Nous allons enlever tous les espaces autours GRUNDSTELLUNG+Spruchschlussel chiffré
def getStartPos():
    global key1

    # Si la clé n'est pas vide, nous allons la transformer en une liste puis enlever les caractères indésirables
    if key1 is not None:
        listkey = list(key1)

        temp = []
        for i in range(0, len(listkey)):
            if 64 < ord(listkey[i]) < 91:
                temp.append(listkey[i])

        key1 = ''.join(car for car in temp)
        return temp


# Nous allons enlever tous les caractères spéciaux dans les messages
def DelSpecialCharsInFile():
    #   Nous allons regarder tous les messages dans la liste, puis les transformer en liste pour enlever
    #   les caractères indésirables

    global message
    if len(message) != 0:
        temp = []

        for j in range(0, len(message)):
            temp.clear()
            text = list(message[j])
            for i in range(0, len(text)):
                if 65 <= ord(text[i]) <= 90:
                    temp.append(text[i])

            message[j] = ''.join(car for car in temp)
