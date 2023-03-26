# File imports
import rotors
import reflector
import plugboard
import files

# Python builtins imports
import os
import datetime

# Bibliothéque pour l'utilisation de graphes
import networkx as nx
import matplotlib.pyplot as plt

# Réglages actuels de la machine Enigma I
wheel_order = ["I", "II", "III"]
start_pos = ["A", "A", "A"]
anneau = [1, 1, 1]
reflecteur = "B"
message = None
secret_mess = None
list_connexion = []

# Objets composant la machine, ici sont représenté les rotors, le tableau de connexion et le réflecteur
tab_de_connexion_O = plugboard.Connexion()
rotor_O = rotors.Rotor()
reflecteur_O = reflector.Reflecteur()

progress_var = 0

# Varibles et structure pour l'attaque
G = nx.DiGraph()
G.add_nodes_from(range(1, 26))
Motif_decomposition_1 = []


# On règle la machine Enigma sur les paramètres choisis (atuels)
def regler():
    tab_de_connexion_O.echange(list_connexion)
    rotor_O.choix(wheel_order)
    rotor_O.reglage(start_pos, anneau)
    reflecteur_O.choix(reflecteur)


def regler2(lst):
    tab_de_connexion_O.echange(list_connexion)
    rotor_O.choix2(lst)
    rotor_O.reglage(start_pos, anneau)
    reflecteur_O.choix(reflecteur)

# Cette fonction permet d'avoir des espaces autours du message chaque 5 lettres,
# C'est-à-dire : 'HELLOWORLDIM' devient 'HELLO WORLD IM'
def decoupage(mess):
    lst = list(mess)
    lst_avec_espace = []
    cpt = 0
    for element in lst:
        if cpt == 5:
            lst_avec_espace.append(" ")
            cpt = 0

        lst_avec_espace.append(element)
        cpt = cpt + 1

    # On transforme la liste des caractères dans un string
    message_espace = ''.join(car for car in lst_avec_espace)
    return message_espace


# Cette fonction permet à partir d'une chaine de caractere en paramètre de retourner son chiffré par Enigma à partir de ses paramètres actuels
# Chiffré retourné en bloc de 5 caractères (C'est-à-dire : 'HELLOWORLDIM' deviendrait 'HELLO WORLD IM')
# Paramètre : mess la chaine de caractère à chiffrer
def chiffrer(mess):
    global start_pos

    # strip supprime les caractères espaces présent en début et fin d'une chaîne
    mess = mess.strip()

    arraymess = list(mess)
    # On chiffre les cacratères de la chaîne un à un
    for i in range(len(arraymess)):
        start_pos = rotor_O.rotation()  # On change la position des rotors au début de chaque caractère à chiffrer
        arraymess[i] = tab_de_connexion_O.chiffrement(arraymess[i])
        arraymess[i] = rotor_O.chiffrement(arraymess[i], reflecteur_O)
        arraymess[i] = tab_de_connexion_O.chiffrement(arraymess[i])

    secret = ''.join(str(car) for car in arraymess)
    # On retourne le message chiffré avec des blocs de 5 caractères
    # C'est-à-dire : 'HELLOWORLDIM' deviendrait 'HELLO WORLD IM'
    secret = decoupage(secret)
    return secret


# Cette fonction permet à partir d'une chaine de caractere en paramètre de retourner son chiffré par Enigma à partir de ses paramètres actuels
# Paramètre : mess la chaine de caractère à chiffrer
def chiffrer_sd(mess):
    global start_pos
    mess = mess.strip()

    arraymess = list(mess)
    for i in range(len(arraymess)):
        start_pos = rotor_O.rotation()
        arraymess[i] = tab_de_connexion_O.chiffrement(arraymess[i])
        arraymess[i] = rotor_O.chiffrement(arraymess[i], reflecteur_O)
        arraymess[i] = tab_de_connexion_O.chiffrement(arraymess[i])

    secret = ''.join(str(car) for car in arraymess)
    return secret


# Cette fonction permet de chiffrer/déchiffrer un fichier et ne retourne rien
# Paramètre : name le nom du fichier dans lequel le fichier sera chiffré/déchiffré
def encryptAndwriteInFile(name):
    # Ouvrir le fichier, s'il n'existe pas il sera crée
    file_decoded = open(name, "w")

    # On récupère la date actuelle, puis on concatène l'heure et les minutes
    currentDT = datetime.datetime.now()
    current_time = str(currentDT.hour) + str(currentDT.minute)

    # On ajoute l'entête dans le fichier
    file_decoded.write(str(current_time) + "=")
    file_decoded.write(str(files.nb_part) + "=")
    file_decoded.write(str(files.part) + "=")
    file_decoded.write(str(files.nb_car) + "=")
    file_decoded.write(str(files.key1) + "\n")
    file_decoded.write(str(files.kengruppen) + " ")

    # Nous allons chiffrer / déchiffrer le fichier
    for ligne in files.message:
        # On récupère une ligne du message du fichier
        lireMessage = chiffrer(ligne)
        # On met le message chiffré/déchiffré dans le fichier
        file_decoded.write(lireMessage + "\n")

    # On ferme le fichier
    file_decoded.close()


# Fonction qui permet de créer un fichier .txt représentant la strucuture d'un message Enigma
# Paramètre : path le nom de la destination dans lequel le fichier sera enregistré
def generation_Fichier(path):
    type = open(path, "w")
    type.write("94 = 1tl = 1tl = 8 = ABCABC\nNOTHH\n\nVOUS POUVEZ SAISIR VOTRE MESSAGE ICI EN MAJUSCULE UNIQUEMENT")
    type.close()


# Fonction qui permet de chiffrer un fichier en utilisant la même méthode utilisé au temps ou Turing et son équipe essayaient de casser Enigma
# Paramètre : file_enter le fichier à chiffrer, file_des le fichier dans lequel le contenu de file_enter sera chiffré
def chiffrement_ameliore(file_enter, file_des):
    with open(file_enter, "r") as file:

        # On récupère l'entête du fichier et le message
        files.ReadFile(file)

        # Enlèves les caractères spéciaux dans le fichier
        # (Il ne doit y avoir que les lettres en majuscule)
        files.DelSpecialCharsInFile()

        # On récupère la concaténation du Grundstellung et Spruchschlussel chiffré
        keyfile = files.getStartPos()

        # Supprimer le contenu de la liste qui contient la position actuelle des rotors
        # Puis, on récupère le Grundstellung
        start_pos.clear()
        for i in range(0, 3):
            start_pos.append(keyfile[i])

        # Mettre à jour les rotors sur les nouvelles positions pour récupérer le Spruchschlussel déchiffré (la vraie clé)
        regler()

        # Récupérer la vraie clé
        realkey = chiffrer(files.key1[-3:])

        # Nous allons supprimer le contenu de la liste de la position actuel du fichier
        # Puis, on met la vraie clé dans la liste
        text = files.key1[-3:]
        start_pos.clear()
        for j in range(0, 3):
            start_pos.append(text[j])

        # Après la récupération de la vraie clé, nous allons déchiffrer/chiffrer le fichier
        # Nous réglons les rotors sur les nouvelles configurations
        regler()

        # Nous allons chiffrer/déchiffrer le fichier
        #
        # puis mettre le résultat dans un autre fichier
        files.key1 = files.key1[0:3] + realkey
        encryptAndwriteInFile(file_des)

        file.close()


# Fonction qui permet de déchiffrer un fichier en utilisant la même méthode utilisé au temps ou Turing et son équipe essayaient de casser Enigma
# Paramètre : file_enter le fichier à déchiffrer, file_des le fichier dans lequel le contenu de file_enter sera déchiffré
def dechiffrement_ameliore(file_enter, file_des):
    with open(file_enter, "r") as file:

        # On récupère l'entête du fichier et le message
        files.ReadFile(file)

        # Enlèves les caractères spéciaux dans le fichier
        # (Il ne doit y avoir que les lettres en majuscule)
        files.DelSpecialCharsInFile()

        # On récupère la concaténation du Grundstellung et Spruchschlussel chiffré
        keyfile = files.getStartPos()

        # Supprimer le contenu de la liste qui contient la position actuelle des rotors
        # Puis, on récupère le Grundstellung
        start_pos.clear()
        for i in range(0, 3):
            start_pos.append(keyfile[i])

        # Mettre à jour les rotors sur les nouvelles positions pour récupérer le Spruchschlussel déchiffré (la vraie clé)
        regler()

        # Récupérer la vraie clé
        realkey = chiffrer(files.key1[-3:])

        # Nous allons supprimer le contenu de la liste de la position actuel du fichier
        # Puis, on met la vraie clé dans la liste
        start_pos.clear()
        for j in range(0, 3):
            start_pos.append(realkey[j])
        # Après la récupération de la vraie clé, nous allons déchiffrer/chiffrer le fichier
        # Nous réglons les rotors sur les nouvelles configurations
        regler()

        # Nous allons chiffrer/déchiffrer le fichier
        #
        # puis mettre le résultat dans un autre fichier
        files.key1 = files.key1[0:3] + realkey
        encryptAndwriteInFile(file_des)
        file.close()


# Fonction qui permet de chiffrer un fichier en utilisant la même méthode utilisé au temps ou Rejewski et son équipe essayaient de casser Enigma
# Paramètre : file_enter le fichier à chiffrer, file_des le fichier dans lequel le contenu de file_enter sera chiffré
def chiffrement_non_ameliore(file_enter, file_des):
    with open(file_enter, "r") as file:
        # On récupère l'entête du fichier et le message
        files.ReadFile(file)

        # Enlèves les caractères spéciaux dans le fichier
        # (Il ne doit y avoir que les lettres en majuscule)
        files.DelSpecialCharsInFile()

        key = files.key1
        key = key.replace(" ", "")
        for i in range(0, 3):
            start_pos.append(key[i])
        regler()

        key2 = key[3] + key[4] + key[5]

        files.key1 = chiffrer_sd(key2+key2)

        start_pos.clear()
        for i in range(3, 6):
            start_pos.append(key[i])

        regler()

        encryptAndwriteInFile(file_des)

        file.close()




# Fonction qui permet de déchiffrer un fichier en utilisant la même méthode utilisé au temps ou Rejewski et son équipe essayaient de casser Enigma
# Paramètre : file_enter le fichier à déchiffrer, file_des le fichier dans lequel le contenu de file_enter sera déchiffré
def dechiffrement_non_ameliore(file_enter, file_des):
    with open(file_enter, "r") as file:
        # On récupère l'entête du fichier et le message
        files.ReadFile(file)

        # Enlèves les caractères spéciaux dans le fichier
        # (Il ne doit y avoir que les lettres en majuscule)
        files.DelSpecialCharsInFile()

        regler()

        pos = start_pos

        key = chiffrer_sd(files.key1)

        files.key1 = pos[0] + pos[1] + pos[2] + key[0] + key[1] + key[2]

        start_pos.clear()
        for i in range(3, 6):
            start_pos.append(key[i])

        regler()

        encryptAndwriteInFile(file_des)

        file.close()


# ******************************************ATTAQUE******************************************


# Génération de fichiers nécessaire pour l'attaque
# Nous générons des fichiers qui simulent l'interception de messages
def generation_fichier_interceptes(key, des):
    global anneau, start_pos

    # save des anneaux, a enlever apres amélioration (voir commentaires ci-dessous)
    ring1 = anneau[0]
    ring2 = anneau[1]
    ring3 = anneau[2]

    anneau = [1, 1,
              1]  # IL EST IMPERATIF DE REVOIR CETTE LIGNE -> ICI ON AIDE LE CALCUL EN ENEVANT LA POSITION DES ANNEAUX SUR LES FICHIERS GENERES
    # SI ON LES LAISSE ON OBTIENDRA UNE POSITION DES ROTORS AVEC (x1,x2,x3) qui sont en réalité (x1-pos1+1,x2-pos2+1,x3-pos3+1)
    # Ce qui changera l'attaque des anneaux
    # Relire articles

    cpt = 1

    # Triplets de lettres utilisées pour chiffré le message qui est ici "soit disant intercepté"
    key1 = 65
    key2 = 66
    key3 = 67

    # On pose les élements du fichier
    text = "SIMONETFATIMANESOUHAITENTPASQUEQUELQUUNPUISSELIRECEMESSAGE"
    files.message.clear()
    files.message.append(text)

    files.nb_part = "1tl"
    files.part = "1tl"
    files.nb_car = len(files.message) + 5
    files.kengruppen = "AGYST"  # hasard

    # on creer le dossier Interception, s'il n'existe pas
    path = str(des + "/Interception/")
    if not os.path.exists(path):
        os.makedirs(path)

    while cpt != 27:
        name = des + "/Interception/" + str(cpt) + ".enigmaI"

        # On positionne les rotors sur la position du jour
        start_pos.clear()
        for i in range(0, 3):
            start_pos.append(key[i])
        regler()

        key4 = chr(key1) + chr(key2) + chr(key3) + chr(key1) + chr(key2) + chr(key3)

        # On la clé chiffré du message
        files.key1 = chiffrer_sd(key4)  # On chiffre les 2 trigrammes qui représente la faille sur laquelle on va attaquer

        # On repositionne les rotors 
        start_pos.clear()
        for i in range(0, 3):
            start_pos.append(key4[i])
        regler()

        encryptAndwriteInFile(name)

        # On essaie pour chaque incrémentation de boucle à obtenir des keys différentes
        # De ce fait on génére 26 fichiers avec un key1 différent pour obtenir les 26 permutations possibles
        # Afin d'obtenir la permutation (σρ‴ρ^(−1)σ) 
        key1 = key1 + 1
        if key1 == 91:
            key1 = 65

        # Les key2 et key3 n'ont pas d'intéret ici hormis le fait de pouvoir obtenir les permutations (σp^5ρ^2 (−1)σ) et (σp^6ρ^3 (−1)σ)
        key2 = key2 + 1
        if key2 == 91:
            key2 = 65
        key3 = key3 + 1
        if key3 == 91:
            key3 = 65

        cpt = cpt + 1

    # # save des anneaux, à enlever apres amélioration
    anneau[0] = ring1
    anneau[1] = ring2
    anneau[2] = ring3


# Attaque sur Enigma basé sur les deux sources suivantes :
#       https://images.math.cnrs.fr/La-machine-Enigma.html?lang=fr
#       https://www.cs.umd.edu/~waa/414-F11/IntroToCrypto.pdf

# Cette première attaque permet d'obtenir à partir de plusieurs fichiers interceptés 
# et un fichier chiffré à partir des méthodes utilisés avant la publication des travaux de Rejewski
# la position des rotors, des anneaux et le choix des rotors utilisé pour chiffré le message dans ce fichier.
def attaque_1(des, fileattaque, lock, condition):
    global anneau, start_pos, progress_var

    # On stockera dans cette liste
    Res = []

    Motif_decomposition_1.clear()

    # On quitte l'attaque si le dossier qui contient les fichiers interceptés n'est pas trouvé
    if not os.path.exists(str(des)):
        print("Dossier inexistant, attaque impossible")
        return 1

    # À partir des fichiers interceptés on cherche à obtenir les motifs de décomposition résultant
    cpt = 1
    key = ""
    while cpt != 27:
        file_name = des + "/" + str(cpt) + ".enigmaI"
        try:
            with open(file_name, "r") as file:
                ligne = file.readline()
                ligne = ligne.split("=")

                if len(ligne) == 5:
                    key = ligne[4]
                    key = key.rstrip()
                else:
                    print("Erreur")

                val1 = ord(key[0]) - 65
                # val2 = ord(key[1]) - 65
                # val3 = ord(key[2]) - 65
                val4 = ord(key[3]) - 65
                # val5 = ord(key[4]) - 65
                # val6 = ord(key[5]) - 65

                G.add_edge(val1 + 1, val4 + 1)

                file.close()

        except IOError:
            print("Fichier introuvable")
            return -1

        cpt = cpt + 1

    # On cherche les composantes fortement connexes dans le graphe
    components = nx.strongly_connected_components(G)

    # On cherche à obtenir les motifs de decomposition du graphe
    for component in components:
        Motif_decomposition_1.append(len(component))

    # Le début de l'attaque grâce à la connnaissance des motifs de décomposition peut démarrer

    # Graphe temporaire qui va permettre de comparer les motifs de décompositon
    G2 = nx.DiGraph()
    G2.add_nodes_from(range(1, 26))
    Motif_decomposition = []

    # Cette triple boucle permet de tester les 60 positions différentes des rotors
    # Nous ne pouvons réduire le nombre d'énumérations possibles pour attaquer la position des rotors
    # Il faut en fait réaliser l'attaque 60 fois, pour chaque position des rotors
    #ici # for a in range(1, 6):
    #ici #     for b in range(1, 6):
    #ici #         for c in range(1, 6):
    # Il n'y a pas de répétion dans le choix des rotors, si on choisit le rotor I en position 1 il ne peut pas figurer en position 3 en même temps
    # Il y a parmi 6^3 possibilités 60 positions possibles pour les rotors qui répondent aux critères de cette condition
    #ici # if c != b and c != a and b != a :
    # Permet de régler dans Enigma la position des rotors
    #ici # liste = [a, b, c]
    # on teste toutes la position deq rotors pour trouver un motif de decomposition correspondant
    cpt = 1
    e1 = 65
    e2 = 65
    e3 = 65
    while cpt != (26 * 26 * 26 + 1):
        # On fait avancer la barre de progression
        lock.acquire()
        progress_var += 1

        if progress_var >= 352:
            condition.notify()

        while progress_var >= 352:
            condition.wait()
        lock.release()

        # On reset la position des anneaux
        anneau = [1, 1, 1]
        cpt2 = 1
        G2.clear()

        # On construit toutes les arcs possibles du graphe représentant les permutations associé à la clé utilisé dans le fichier a attaquer
        while cpt2 != 27:
            # On reset la position des rotors
            start_pos.clear()
            start_pos.append(chr(e1))
            start_pos.append(chr(e2))
            start_pos.append(chr(e3))
            # On régle la positon des rotors
            regler()
            #ici regler2()

            alpha = chr(cpt2 + 64)
            carac = chiffrer(alpha + alpha + alpha + alpha)  # le premier alpha et le dernier alpha sont utiles
            val1 = ord(carac[0]) - 64
            val2 = ord(carac[3]) - 64
            G2.add_edge(val1, val2)

            cpt2 = cpt2 + 1

        # On cherche les composantes fortement connexes dans le graphe temporaire
        components = nx.strongly_connected_components(G2)
        # On cherche à obtenir les motifs de decomposition du graphe
        Motif_decomposition.clear()
        for component in components:
            Motif_decomposition.append(len(component))
        

        flag = 0
        # p le nombre de motif de décomposition dans le graphe que l'on vient de construire
        p = len(Motif_decomposition)

        # On cherche à savoir si le graphe a un motif de decomposition simulaire à celui que l'on cherche
        if p == len(Motif_decomposition_1):
            for i in range(0, p):
                if Motif_decomposition_1[i] != Motif_decomposition[i]:
                    flag = 1
                    break
        # Si ce n'est pas le cas alors la clé actuel n'est pas la bonne
        # Alors on essaie une autre clé
        else:
            flag = 1

        # Si le graphe a un motif de decomposition simulaire à celui que l'on cherche
        if flag == 0:
            # On cherche à comparer les permutations afin d'obtenir la bonne clé
            # Si les motifs de permutations sont identiques sur les deux graphes alors cela signifie que la clé actuel est possiblement
            # celle utilisé pour chiffré le message (on considère que les fichiers interceptés ont été chiffrés avec les mêmes réglages 
            # que le fichier que l'on va attaquer)
            for i in range(1, 26):
                x1 = list(G.successors(i))
                x2 = list(G2.successors(i))
                if x1[0] != x2[0]:
                    flag = 1
                    break

        # On attaque maintenant les anneaux
        if flag == 0:
            # On cherche le fichier à attaquer
            with open(fileattaque, "r") as file:
                ligne = file.readline()
                ligne = ligne.split("=")

                if len(ligne) == 5:
                    entete = ligne[4]
                    entete = entete.rstrip()
                else:
                    print("Erreur")
                file.close()
            
            # On teste toutes les positions des anneaux et on vérifie si dans l'entête 123456, les valeurs 1 = 4, 2 = 5, 3 = 6
            # Ce qui signifiera que la clé testé est correct
            cpt5 = 1
            e4 = 1
            e5 = 1
            e6 = 1
            while cpt5 != 26 * 26 * 26 + 1:
                # On régle les anneaux
                anneau = [e4, e5, e6]
                # On reset la position des rotors
                start_pos.clear()
                start_pos.append(chr(e1))
                start_pos.append(chr(e2))
                start_pos.append(chr(e3))
                regler()
                #ici  regler2(liste)

                res = chiffrer(entete)

                # si dans l'entête 123456, les valeurs 1 = 4, 2 = 5, 3 = 6. Ce qui signifiera que la clé testé est correct
                if res[0] == res[3] and res[1] == res[4] and res[2] == res[6]:
                    #ici # print(liste)
                    #ici # Res.append(liste)
                    print("Solution : " + chr(e1) + " " + chr(e2) + " " + chr(e3))
                    Res.append(str(chr(e1)) + " " + str(chr(e2)) + " " + str(chr(e3)))
                    print("Solution anneau: " + str(e4) + " " + str(e5) + " " + str(e6))
                    Res.append(str(e4) + " " + str(e5) + " " + str(e6))

                # On essaie tous les anneaux pour toutes les positions
                e4 = e4 + 1
                if e4 == 27:
                    e4 = 1
                    e5 = e5 + 1
                    if e5 == 27:
                        e5 = 1
                        e6 = e6 + 1

                cpt5 = cpt5 + 1  # here

        # On essaie tous les rotors pour toutes les positions
        e3 = e3 + 1
        if e3 == 91:
            e3 = 65
            e2 = e2 + 1
            if e2 == 91:
                e2 = 65
                e1 = e1 + 1
        cpt = cpt + 1

    # Si les autres threads ne sont pas actives, on doit les réveiller
    lock.acquire()
    condition.notify()
    lock.release()
    print("Attaque terminé")
    return Res

# On représente de façon graphique les orbites induite par la lecture des fichiers interceptées,
# C'est à partir de ces orbites que les motifs de décomposition ont été calculés pour attaquer le fichier durant l'attaque 1
def graphe():
    nx.draw(G, with_labels=True)
    plt.show()

# Fonction qui permet d'échanger deux paires de lettres dans un message,
# Par exemple si let1 = a et let2 = b, toutes les occurences de a dans le message sera remplacé par b et inversement.
def permute_deux_lettres(m, let1, let2):
    ligne_as_list = list(m)

    if len(ligne_as_list) != 0:

        for i in range(0, len(ligne_as_list)):
            if ligne_as_list[i] == let1:
                ligne_as_list[i] = let2
            else:
                if ligne_as_list[i] == let2:
                    ligne_as_list[i] = let1

        m = ''.join(alpha for alpha in ligne_as_list)

    return m

#Fonction qui permet de calculer la statistique de Sinkov en francais d'un message m
def Sinkov_stat(m):
    # fi english
    fi = [8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153, 0.772, 4.025, 2.406, 6.749, 7.507,
           1.929, 0.095, 5.987, 6.327, 9.056, 2.758, 0.978, 2.360, 0.150, 1.974, 0.074]

    # frequence d'apparition des lettres en francais
    #fi = [8.15, 0.97, 3.15, 3.73, 17.39, 1.12, 0.97, 0.85, 7.31, 0.45, 0.02, 5.69, 2.87, 7.12, 5.28, 2.80, 1.21, 6.64, 8.14, 7.22, 6.38, 1.64, 0.03, 0.41, 0.28, 0.15]

    ni = [0] * 26
    s = 0
    for elt in m:
        ni[ord(elt) - 65] += 1

    for i in range(0, 26):
        ni[i] /= len(m)

    for i in range(0, 26):
        s += ni[i] * fi[i]  # ((ni[i]-fi[i])*(ni[i]-fi[i]))/fi[i]
    return s

# Attaque sur Enigma basé sur les deux sources suivantes :
#       https://images.math.cnrs.fr/La-machine-Enigma.html?lang=fr
#       https://www.cs.umd.edu/~waa/414-F11/IntroToCrypto.pdf

# Cette deuxième attaque permet d'obtenir un probable (avec une grosse quantite de texte) tableau de connexion utilisé pour
# chiffré le message dans ce fichier.
def attaque_2(fileattaque):
    global start_pos, list_connexion

    list_connexion = []
    # On cherche le texte que compose le fichier
    ligne = ""
    cpt = 0
    message = ""
    with open(fileattaque, "r") as file:
        for ligne in file:
            if cpt != 0: # On passe l'entete
                if len(ligne) == 1: 
                    continue # On passe les lignes vides
                if cpt == 1: #A la premiere ligne non vide on ne considère pas les 5 premiers caractères
                    temp = list(ligne)
                    for i in range(0,5):
                        del temp[0]
                    ligne = ""
                    ligne = "".join(temp)
                ligne = ligne.replace(" ","")
                ligne = ligne.replace("\n","")
                message = message + ligne
            cpt+=1
        file.close()


    maximum = float('-inf')
    maximumRet = float('-inf')
    lettre_retenue1 = None
    lettre_retenue2 = None
    gama = []
    flag = 0

    while flag == 0:
        lettre1 = "A"
        lettre2 = "A"
        maximum = float('-inf')
        minimum = float('inf')
        lettre_retenue1 = None
        lettre_retenue2 = None
        lim = 26  # max - 1
        lim2 = 26

        # On test toutes les inversions de lettres possibles dans le message
        for j in range(1, lim):
            for i in range(1, lim2):

                lettre2 = chr(ord(lettre2) + 1)

                messageSave = message

                # On inverse les lettres dans le chiffré 
                messageSave = permute_deux_lettres(messageSave, lettre1, lettre2)
                start_pos = ["A", "A", "A"]
                regler()
                # On le chiffre pour obtenir le texte en clair
                messageSave = chiffrer_sd(messageSave)
                # On permute les lettres dans le clair
                messageSave = permute_deux_lettres(messageSave, lettre1, lettre2)

                # On test la statistique de Sinkov dans le message 
                s = Sinkov_stat(messageSave)

                # Si on obtient une valeur statistique supérieure à la précédente, alors on retient les lettres qui permettent de retenir un message 
                # le plus proche possible d'un texte en français
                if maximum < s:
                    lettre_retenue1 = lettre1
                    lettre_retenue2 = lettre2
                    maximum = s

            # On change les lettres à permutter pour la prochaine permutations de lettres
            lettre1 = chr(ord(lettre1) + 1)
            lettre2 = lettre1
            lim2 -= 1

        # On sauvegarde la permutation de lettres qui a permis d'obtenir la meilleure statistique si c'est le cas
        if maximum > maximumRet:
            gama.append(lettre_retenue1)
            gama.append(lettre_retenue2)
            list_connexion.append(lettre_retenue1 + lettre_retenue2)
            maximumRet = maximum
        else:
            flag = 1

        # On recommence tant qu'on ne trouve pas une meilleur statistique

    for i in range(0, int(len(gama)), 2):
        print(gama[i] + " <-> " + gama[i + 1])

    return gama
