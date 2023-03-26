# Déclaration des rotors disponibles dans le modèle I de Enigma
rotor1 = list("EKMFLGDQVZNTOWYHXUSPAIBRCJ")
rotor1_notch = "Q"
rotor2 = list("AJDKSIRUXBLHWTMCQGZNPYFVOE")
rotor2_notch = "E"
rotor3 = list("BDFHJLCPRTXVZNYEIWGAKMUSQO")
rotor3_notch = "V"
rotor4 = list("ESOVPZJAYQUIRHXLNFTGKDCMWB")
rotor4_notch = "J"
rotor5 = list("VZBRGITYUPSDNHLXAWMJQOFECK")
rotor5_notch = "Z"

# Fonction qui permet à partir d'une liste de passer sa tête en bout de la liste (dernier élément)
def rota(lst):
    tmp = lst[0]
    del lst[0]
    lst.append(tmp)

# Fonction qui permet à partir d'une liste de passer son dernier element en tête de liste
def rota2(lst):
    lst.insert(0, lst.pop())

# Classe qui définit les rotors positionnés dans la machine
class Rotor:
    def __init__(self):
        self.rotorC1_0 = 0          # Position du rotor 1 sur la machine
        self.rotorC1 = []           # Liste des 26 caractères du rotor 1, en tête de liste le caractère associé à la position du rotor
        self.rotorC1_notch = None   # Caractère où se situe l'encoche sur le rotor 1
        self.anneauC1 = 0           # Position de l'anneau sur le rotor 1
        self.rotorC2_0 = 0          # Position du rotor 2 sur la machine
        self.rotorC2 = []           # Liste des 26 caractères du rotor 2, en tête de liste le caractère associé à la position du rotor
        self.rotorC2_notch = None   # Caractère où se situe l'encoche sur le rotor 2
        self.anneauC2 = 0           # Position de l'anneau sur le rotor 2
        self.rotorC3_0 = 0          # Position du rotor 3 sur la machine
        self.rotorC3 = []           # Liste des 26 caractères du rotor 3, en tête de liste le caractère associé à la position du rotor
        self.rotorC3_notch = None   # Caractère où se situe l'encoche sur le rotor 3
        self.anneauC3 = 0           # Position de l'anneau sur le rotor 3

    # Fonction qui permet de faire correspondre les rotors sélectionnés par un utilisateur en fonction du choix des rotors qu'il souhaite utiliser
    # Paramètre : Liste des 3 rotors sectionnée par l'utilisateur en chiffre romain
    def choix(self, liste):
        global rotor1, rotor1_notch, rotor2, rotor2_notch, rotor3, rotor3_notch, rotor4, rotor4_notch, rotor5, rotor5_notch
        rotor1 = list("EKMFLGDQVZNTOWYHXUSPAIBRCJ")
        rotor1_notch = "Q"
        rotor2 = list("AJDKSIRUXBLHWTMCQGZNPYFVOE")
        rotor2_notch = "E"
        rotor3 = list("BDFHJLCPRTXVZNYEIWGAKMUSQO")
        rotor3_notch = "V"
        rotor4 = list("ESOVPZJAYQUIRHXLNFTGKDCMWB")
        rotor4_notch = "J"
        rotor5 = list("VZBRGITYUPSDNHLXAWMJQOFECK")
        rotor5_notch = "Z"
        cpt = 1
        # Pour tous les rotors selectionné
        for element in liste:
            # Association des nombres romains en nombres arabes
            elt = None
            match element:
                case "I":
                    elt = 1
                case "II":
                    elt = 2
                case "III":
                    elt = 3
                case "IV":
                    elt = 4
                case "V":
                    elt = 5

            # Association des rotors choisis dans la machine : rotorC1, rotorC2 et rotorC3 prennent respectivement un rotor disponible dans le modèle I de Enigma
            match elt:
                case 1:
                    match cpt:
                        case 1:
                            self.rotorC1 = rotor1
                            self.rotorC1_notch = rotor1_notch
                        case 2:
                            self.rotorC2 = rotor1
                            self.rotorC2_notch = rotor1_notch
                        case 3:
                            self.rotorC3 = rotor1
                            self.rotorC3_notch = rotor1_notch
                    cpt = cpt + 1
                case 2:
                    match cpt:
                        case 1:
                            self.rotorC1 = rotor2
                            self.rotorC1_notch = rotor2_notch
                        case 2:
                            self.rotorC2 = rotor2
                            self.rotorC2_notch = rotor2_notch
                        case 3:
                            self.rotorC3 = rotor2
                            self.rotorC3_notch = rotor2_notch
                    cpt = cpt + 1
                case 3:
                    match cpt:
                        case 1:
                            self.rotorC1 = rotor3
                            self.rotorC1_notch = rotor3_notch
                        case 2:
                            self.rotorC2 = rotor3
                            self.rotorC2_notch = rotor3_notch
                        case 3:
                            self.rotorC3 = rotor3
                            self.rotorC3_notch = rotor3_notch
                    cpt = cpt + 1
                case 4:
                    match cpt:
                        case 1:
                            self.rotorC1 = rotor4
                            self.rotorC1_notch = rotor4_notch
                        case 2:
                            self.rotorC2 = rotor4
                            self.rotorC2_notch = rotor4_notch
                        case 3:
                            self.rotorC3 = rotor4
                            self.rotorC3_notch = rotor4_notch
                    cpt = cpt + 1
                case 5:
                    match cpt:
                        case 1:
                            self.rotorC1 = rotor5
                            self.rotorC1_notch = rotor5_notch
                        case 2:
                            self.rotorC2 = rotor5
                            self.rotorC2_notch = rotor5_notch
                        case 3:
                            self.rotorC3 = rotor5
                            self.rotorC3_notch = rotor5_notch
                    cpt = cpt + 1
                case _:
                    exit("Erreur dans la sélection des choix des rotors")
        return 0
    
    #pareil sans choix romain
    def choix2(self, liste):
        global rotor1, rotor1_notch, rotor2, rotor2_notch, rotor3, rotor3_notch, rotor4, rotor4_notch, rotor5, rotor5_notch
        rotor1 = list("EKMFLGDQVZNTOWYHXUSPAIBRCJ")
        rotor1_notch = "Q"
        rotor2 = list("AJDKSIRUXBLHWTMCQGZNPYFVOE")
        rotor2_notch = "E"
        rotor3 = list("BDFHJLCPRTXVZNYEIWGAKMUSQO")
        rotor3_notch = "V"
        rotor4 = list("ESOVPZJAYQUIRHXLNFTGKDCMWB")
        rotor4_notch = "J"
        rotor5 = list("VZBRGITYUPSDNHLXAWMJQOFECK")
        rotor5_notch = "Z"
        cpt = 1
        # Pour tous les rotors selectionné
        for element in liste:
            # Association des rotors choisis dans la machine : rotorC1, rotorC2 et rotorC3 prennent respectivement un rotor disponible dans le modèle I de Enigma
            match element:
                case 1:
                    match cpt:
                        case 1:
                            self.rotorC1 = rotor1
                            self.rotorC1_notch = rotor1_notch
                        case 2:
                            self.rotorC2 = rotor1
                            self.rotorC2_notch = rotor1_notch
                        case 3:
                            self.rotorC3 = rotor1
                            self.rotorC3_notch = rotor1_notch
                    cpt = cpt + 1
                case 2:
                    match cpt:
                        case 1:
                            self.rotorC1 = rotor2
                            self.rotorC1_notch = rotor2_notch
                        case 2:
                            self.rotorC2 = rotor2
                            self.rotorC2_notch = rotor2_notch
                        case 3:
                            self.rotorC3 = rotor2
                            self.rotorC3_notch = rotor2_notch
                    cpt = cpt + 1
                case 3:
                    match cpt:
                        case 1:
                            self.rotorC1 = rotor3
                            self.rotorC1_notch = rotor3_notch
                        case 2:
                            self.rotorC2 = rotor3
                            self.rotorC2_notch = rotor3_notch
                        case 3:
                            self.rotorC3 = rotor3
                            self.rotorC3_notch = rotor3_notch
                    cpt = cpt + 1
                case 4:
                    match cpt:
                        case 1:
                            self.rotorC1 = rotor4
                            self.rotorC1_notch = rotor4_notch
                        case 2:
                            self.rotorC2 = rotor4
                            self.rotorC2_notch = rotor4_notch
                        case 3:
                            self.rotorC3 = rotor4
                            self.rotorC3_notch = rotor4_notch
                    cpt = cpt + 1
                case 5:
                    match cpt:
                        case 1:
                            self.rotorC1 = rotor5
                            self.rotorC1_notch = rotor5_notch
                        case 2:
                            self.rotorC2 = rotor5
                            self.rotorC2_notch = rotor5_notch
                        case 3:
                            self.rotorC3 = rotor5
                            self.rotorC3_notch = rotor5_notch
                    cpt = cpt + 1
                case _:
                    exit("Erreur dans la sélection des choix des rotors")
        return 0
    


    # Méthode qui permet de fournir le caractère de sortie vers le rotor 2 à partir du tableau de connexion en fonction des réglages de la machine
    # Paramètre : b le caractère d'entrée dans le rotor 3 depuis le tableau de connexion
    def chiffrement3(self, b):

        # On cherche l'indice du caractère qui associe le caractère de sortie au caractère d'entrée
        # Par exemple b = 'H', rotorC3 = "VZBRGITYUPSDNHLXAWMJQOFECK"
        #                                "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        # L'indice associé à l'indice H est : 7 (A = 0 et Z = 25)
        # Le caractère associé à cette indice est Y
        # La méthode retournera ici le caractère Y

        c = ord(b)
        if 65 <= c <= 90: # Condition toujours vérifié (la bonne saisie des informations est déjà vérifié)
            c = c - 65

        return self.rotorC3[c]

    # Méthode qui permet de fournir le caractère de sortie vers le rotor 1 à partir du rotor 3 en fonction des réglages de la machine
    # Paramètre : b le caractère d'entrée dans le rotor 2 depuis le rotor 3
    def chiffrement2(self, b):
        # On cherche l'indice du caractère qui associe le caractère de sortie au caractère d'entrée
        # Par exemple b = 'H', rotorC2 = "VZBRGITYUPSDNHLXAWMJQOFECK"
        #                                "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        # L'indice associé à l'indice H est : 7 (A = 0 et Z = 25)
        # Le caractère associé à cette indice est Y
        # Mais attention il faut ici prendre en compte la position du rotor 3 par rapport au rotor 2
        # Si la rotation du rotor 3 <=> 2 alors l'indice 7 sera ici réduit de 2 pour donner 5
        # Dans ce cas le caractère associé à cette indice est I
        # La méthode retournera ici le caractère I
        c = (ord(b))
        if 65 <= c <= 90:
            c = c - 65

        # On considère la position du rotor 3 par rapport au rotor 2 (décalage des fils physiquement)
        c = c - self.rotorC3_0
        if c < 0:
            c = c + 26

        return self.rotorC2[c]

    # Méthode qui permet de fournir le caractère de sortie vers le réflecteur à partir du rotor 2 en fonction des réglages de la machine
    # Paramètre : b le caractère d'entrée dans le rotor 1 depuis le rotor 2
    def chiffrement1(self, b):
        # Même explications que la méthode "chiffrement2"
        c = (ord(b))
        if 65 <= c <= 90:
            c = c - 65

        # On considère la position du rotor 2 par rapport au rotor 1 (décalage des fils physiquement)
        c = c - self.rotorC2_0
        if c < 0:
            c = c + 26

        return self.rotorC1[c]

    # Méthode qui permet de fournir le caractère de sortie vers le rotor 2 à partir du réflecteur en fonction des réglages de la machine
    # Paramètre : b le caractère d'entrée dans le rotor 1 depuis le réflecteur
    def chiffrement1_0(self, b):
        # On cherche l'indice du caractère qui associe le caractère de sortie au caractère d'entrée
        # Par exemple b = 'H', rotorC1 = "VZBRGITYUPSDNHLXAWMJQOFECK"
        #                                "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        # L'indice associé à l'indice H est : 7 (A = 0 et Z = 25)
        # Mais si le rotor 1 n'est pas à la position 0, il y a un décallage entre la sortie du réflecteur et lui même
        # Il faut donc considérer ce décallage
        # Pour ce faire si la rotation du rotor 1 <=> 2 alors l'indice 7 sera ici augmenté de 2 pour donner 9
        # Dans ce cas la réel sortie de valeur de caractère du réflecteur est équivalente à 9 soit J
        # On a à présent obtenue la vraie sortie du réflecteur
        #
        # On cherche maintenant l'indice du caractère qui associe le caractère de sortie au caractère d'entrée (réel)
        # Nous notons X le caractère associé à cette indice
        # Nous cherchons le caractère (qu'on note Y) de sortie correspondant à X dans le rotor en position 0
        # Nous appliquons ensuite à ce caractère Y le décallage induit par le rotor en fonction de sa position
        # Nous obtenons en conséquence le caractère de sortie attendu

        c = ord(b)

        # On considère la position du rotor 1 par rapport au réflecteur (décalage des fils physiquement)
        c = c + self.rotorC1_0
        if c > 90:
            c = c - 26

        # On cherche à obtenir la lettre de sortie du réflecteur après avoir pris en compte la position physique du rotor 1
        alpha = chr(c)  # On obtient la lettre correspondant à la vraie sortie du réflecteur

        # On cherche maintenant l'indice du caractère qui associe le caractère de sortie au caractère d'entrée (réel)
        # Nous cherchons l'indice du caractère de sortie correspondant dans le rotor en position 0
        c = self.rotorC1.index(alpha)

        # Nous appliquons ensuite à ce caractère le décallage induit par le rotor en fonction de sa position
        c = c + self.rotorC1_0
        c = c + 65
        if c > 90:
            c = c - 26

        # On retourne le caractère de sortie attendu
        return chr(c)

    # Méthode qui permet de fournir le caractère de sortie vers le rotor 3 à partir du rotor 1 en fonction des réglages de la machine
    # Paramètre : b le caractère d'entrée dans le rotor 2 depuis le rotor 1
    def chiffrement2_0(self, b):
        # Même explications que la méthode "chiffrement1_0", hormis une petite différence

        c = ord(b)
        c = c + self.rotorC2_0
        if c > 90:
            c = c - 26

        # La petite différence ici réside dans le fait que nous devons prendre en considération l'alignement
        # du rotor 1 par rapport au rotor 2
        c = c - self.rotorC1_0
        if c < 65:
            c = c + 26

        alpha = chr(c)

        c = self.rotorC2.index(alpha)

        c = c + self.rotorC2_0
        c = c + 65
        if c > 90:
            c = c - 26

        return chr(c)


    # Méthode qui permet de fournir le caractère de sortie vers le tableau de connexion (attention la prise en compte de la position du rotor 3 devra être considéré avant envoie au tableau de connexion) à partir du rotor 2 en fonction des réglages de la machine
    # Paramètre : b le caractère d'entrée dans le rotor 3 depuis le rotor 2
    def chiffrement3_0(self, b):
        # Même explications que la méthode "chiffrement2_0"

        c = ord(b)
        c = c + self.rotorC3_0
        if c > 90:
            c = c - 26

        c = c - self.rotorC2_0
        if c < 65:
            c = c + 26

        alpha = chr(c)

        c = self.rotorC3.index(alpha)

        c = c + self.rotorC3_0
        c = c + 65
        if c > 90:
            c = c - 26

        return chr(c)

    # Méthode qui permet de fournir le caractère chiffré à partir d'un caractère issue du tableau de connexion vers ce même tableau de connexion
    # Dans cette méthode le caractère à chiffrer ce chiffrera en échangeant de caractère après ces différents passage dans le rotor 3, le rotor 2, le rotor 1, le réflecteur et encore une fois dans le rotor 1, le rotor 2 puis le rotor 3
    # Paramètre : b le caractère d'entrée dans le rotor 3 depuis le tableau de connexion
    #             r l'objet reflector utilisé pendant ce processus de chiffrement
    def chiffrement(self, b, r):
        b = self.chiffrement3(b)
        b = self.chiffrement2(b)
        b = self.chiffrement1(b)
        b = r.chiffrement(b, self)
        b = self.chiffrement1_0(b)
        b = self.chiffrement2_0(b)
        b = self.chiffrement3_0(b)

        # Nous devons ici considérer la position du réflecteur 3 pour obtenir une sortie correcte
        e = ord(b)
        e = e - 65
        e = e - self.rotorC3_0
        if e < 0:
            e = e + 26
        e = e + 65

        return chr(e)

    # Méthode qui permet de régler la position des rotors et des anneaux
    # Paramètre : liste de 3 caractères compris entre A et Z correspondant à la position repectivement des rotors 1, 2 et 3
    #             liste de la positions des trois anneaux compris entre 1 et 26
    def reglage(self, liste, anneau):
        self.rotorC1_0 = 0
        self.rotorC2_0 = 0
        self.rotorC3_0 = 0
        cpt = 1
        for element in liste:
            i = 1
            # On associe le caractère à sa position dans l'alphabet
            elt = ord(element) - 64 # A - 64 = 1 et Z - 64 = 90 - 64 = 26
            match cpt:
                # traitement du premier élément de la liste
                case 1:
                    # on effectue elt rotation de 1 sur le rotor
                    while i < elt:
                        rota(self.rotorC1)
                        self.rotorC1_0 = self.rotorC1_0 + 1 # on pourrait poser self.rotorC1_0 = elt (en vérifiant le dépassement de l'intervalle [0,25])
                        if self.rotorC1_0 == 26:
                            self.rotorC1_0 = 0
                        i = i + 1
                    cpt = cpt + 1
                # traitement du deuxième élément de la liste
                case 2:
                    # on effectue elt rotation de 1 sur le rotor
                    while i < elt:
                        rota(self.rotorC2)
                        self.rotorC2_0 = self.rotorC2_0 + 1
                        if self.rotorC2_0 == 26:
                            self.rotorC2_0 = 0
                        i = i + 1
                    cpt = cpt + 1
                # traitement du troisième élément de la liste
                case 3:
                    # on effectue elt rotation de 1 sur le rotor
                    while i < elt:
                        rota(self.rotorC3)
                        self.rotorC3_0 = self.rotorC3_0 + 1
                        if self.rotorC3_0 == 26:
                            self.rotorC3_0 = 0
                        i = i + 1
                    cpt = cpt + 1

        # Reglage de la position des anneaux

        # Variable non utilisées, peut-être utile dans le futur
        self.anneauC1 = anneau[0]
        self.anneauC2 = anneau[1]
        self.anneauC3 = anneau[2]



        # On simule un décallage des "fils" dans le rotors, en décallant la liste des 26 caractères des différents rotors

        cpt = 1
        while cpt != anneau[2]:
            rota2(self.rotorC3)
            cpt = cpt + 1
        cpt = 1

        # On effectue ici le décallage des lettres : 
        # Si position du rotor <=> 3 
        # Alors la lettre A devient C
        # A -> B -> C

        for i in range(len(self.rotorC3)):
            tmp = self.rotorC3[i]
            tmp = ord(tmp) + anneau[2] - 1
            if tmp > 90:
                tmp = tmp - 26
            self.rotorC3[i] = chr(tmp)
            cpt = cpt + 1
        
        # Même opérations sur les deux autre rotors

        cpt = 1
        while cpt != anneau[1]:
            rota2(self.rotorC2)
            cpt = cpt + 1
        cpt = 1
        for i in range(len(self.rotorC2)):
            tmp = self.rotorC2[i]
            tmp = ord(tmp) + anneau[1] - 1
            if tmp > 90:
                tmp = tmp - 26
            self.rotorC2[i] = chr(tmp)
            cpt = cpt + 1

        cpt = 1
        while cpt != anneau[0]:
            rota2(self.rotorC1)
            cpt = cpt + 1
        cpt = 1
        for i in range(len(self.rotorC1)):
            tmp = self.rotorC1[i]
            tmp = ord(tmp) + anneau[0] - 1
            if tmp > 90:
                tmp = tmp - 26
            self.rotorC1[i] = chr(tmp)
            cpt = cpt + 1



    # Méthode qui permet de gérer la gestion des rotations des rotors pendant la procédure de chiffrement
    def rotation(self):
        # Notons ici que le rotor 2 peut tourner dans deux conditions :
        # -Quand le rotor 3 (le plus à droite du point de vue du chiffreur) rencontre l'encoche
        # -Quand le rotor 2 (lui même) rencontre l'encoche

        # On effectue une rotation du rotor 3
        rota(self.rotorC3)
        self.rotorC3_0 = self.rotorC3_0 + 1
        if self.rotorC3_0 == 26:
            self.rotorC3_0 = 0

        # On récupère le caractère visible sur le rotor 3 par le chiffreur avant la rotation du rotor 3
        if self.rotorC3_0 >= 1:
            tmp1 = 65 + self.rotorC3_0 - 1
        else:
            tmp1 = 90

        # On récupère le caractère visible sur le rotor 2 par le chiffreur avant la rotation du rotor 3
        tmp2 = 0
        if self.rotorC2_0 >= 0:
            tmp2 = 65 + self.rotorC2_0

        # Si on rencontre l'enchoche au rotor3 on avance le rotor 2

        # On vérifie si le caractère visible par le chiffreur sur le rotor 3 avant la rotation du rotor 3 correspond à la valeur visible de la notch (du rotor 3)
        # Plus clairement cela signifie que le mécanisme rencontre l'encoche du rotor 3
        # On tourne en conséquence le rotor 2
        if chr(tmp1) == self.rotorC3_notch:
            rota(self.rotorC2)
            self.rotorC2_0 = self.rotorC2_0 + 1
            if self.rotorC2_0 == 26:
                self.rotorC2_0 = 0

        # On vérifie si le caractère visible par le chiffreur sur le rotor 2 avant la rotation du rotor 3 correspond à la valeur visible de la notch (du rotor 2)
        # Plus clairement cela signifie que le mécanisme rencontre l'encoche du rotor 2
        # On tourne en conséquence le rotor 2 et 1
        else:
            if chr(tmp2) == self.rotorC2_notch:

                # rotation rotor 2
                rota(self.rotorC2)
                self.rotorC2_0 = self.rotorC2_0 + 1
                if self.rotorC2_0 == 26:
                    self.rotorC2_0 = 0

                # rotation rotor 1
                rota(self.rotorC1)
                self.rotorC1_0 = self.rotorC1_0 + 1
                if self.rotorC1_0 == 26:
                    self.rotorC1_0 = 0


        # changer affichage
        tmp1 = chr(65 + self.rotorC1_0)
        tmp2 = chr(65 + self.rotorC2_0)
        tmp3 = chr(65 + self.rotorC3_0)
        lst = []
        lst.append(tmp1)
        lst.append(tmp2)
        lst.append(tmp3)
        return lst
    


#FAIRE reculer la position des rotors, méthode inverse de rotation()
    def rotationInverse(self):

        #à -2        
        # Photo du 2 mars
        tmp1 = self.rotorC3_0 + 65 - 2
        if tmp1 < 65:
            tmp1 = tmp1 + 26

        # à -1
        tmp2 = self.rotorC2_0 + 65 - 1
        if tmp2 < 65:
            tmp2 = tmp2 + 26

        #à -1
        tmp3 = self.rotorC3_0 + 65 - 1
        if tmp3 < 65:
            tmp3 = tmp3 + 26


        # rotation inverse du rotor 3
        rota2(self.rotorC3)
        self.rotorC3_0 = self.rotorC3_0 - 1
        if self.rotorC3_0 == -1:
            self.rotorC3_0 = 25


        
        if chr(tmp2) == self.rotorC2_notch and chr(tmp1) == self.rotorC1_notch:
            rota2(self.rotorC1)
            self.rotorC1_0 = self.rotorC1_0 - 1
            if self.rotorC1_0 == -1:
                self.rotorC1_0 = 25

            self.rotorC2_0 = self.rotorC2_0 - 1
            if self.rotorC2_0 == -1:
                self.rotorC2_0 = 25


        else:
            if chr(tmp3) == self.rotorC3_notch:
                rota2(self.rotorC2)
                self.rotorC2_0 = self.rotorC2_0 - 1
                if self.rotorC2_0 == -1:
                    self.rotorC2_0 = 25


        # changer affichage
        tmp1 = chr(65 + self.rotorC1_0)
        tmp2 = chr(65 + self.rotorC2_0)
        tmp3 = chr(65 + self.rotorC3_0)
        lst = []
        lst.append(tmp1)
        lst.append(tmp2)
        lst.append(tmp3)
        return lst