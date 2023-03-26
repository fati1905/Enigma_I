#Déclaration des reflecteurs disponibles dans le modèle I de Enigma
reflecteurA = list("EJMZALYXVBWFCRQUONTSPIKHGD")
reflecteurB = list("YRUHQSLDPXNGOKMIEBFZCWVJAT")
reflecteurC = list("FVPJIAOYEDRZXWGCTKUQSBNMHL")


class Reflecteur:
    global reflecteurA, reflecteurB, reflecteurC

    def __init__(self):
        self.reflecteur =  ""

    def choix(self, reflecteur):
        if reflecteur == "A":
            self.reflecteur = reflecteurA
        
        if reflecteur == "B":
            self.reflecteur = reflecteurB
        
        if reflecteur == "C":
            self.reflecteur = reflecteurC
        return 0

    # Méthode qui permet de fournir le caractère de sortie vers le rotor 1 (retour vers tableau de connexion) à partir du rotor 1 en fonction des réglages de la machine
    # Paramètre : b le caractère d'entrée dans le réflecteur depuis le rotor 1
    def chiffrement(self, b, rotor):
        # Même explications que la méthode "chiffrement2" dans le fichier "rotors.py"
        c1 = (ord(b))
        if c1 >= 65 and c1 <= 90:
            c1 = c1 - 65
        
        # On considère la position du rotor 1 par rapport au réflecteur (décalage des fils physiquement)
        c1 = c1 - rotor.rotorC1_0
        if c1 < 0:
            c1 = c1 + 26

        return self.reflecteur[c1]