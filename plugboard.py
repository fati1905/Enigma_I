# Tableau de connexion
class Connexion:
    def __init__(self):
        self.touche_clavier = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self.connect = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    # Fonction qui fait office de simuler la fonction du tableau de connexion de Enigma I
    def echange(self, liste):

        already_used = []  # Empêche l'échange des mêmes lettres déjà échangées

        # S'assurer que nous allons échanger que 10 lettres
        if len(liste) > 10:
            # print("Vous ne pouvez échanger que 10 lettres, réessayer!")
            return 1

        for element in liste:
            # Convertit AB vers une liste du type ['A', 'B']
            couple = list(element)

            # Si la liste contient trois caractères ABC, alors l'utilisateur doit réessayer
            if len(couple) == 2:
                # Les lettres doivent être comprises entre A et Z
                if (65 <= ord(couple[0]) <= 90) and (65 <= ord(couple[1]) <= 90):

                    # Les lettres ne doivent pas être redondantes
                    if couple[0] in already_used or couple[1] in already_used:
                        # print("Les lettres ne doivent pas être redondantes !")
                        return 1
                    else:
                        self.connect[ord(couple[0]) - 65] = couple[1]
                        self.connect[ord(couple[1]) - 65] = couple[0]

                        # Ajouter les lettres dans la liste des lettres échangées
                        already_used.append(couple[0])
                        already_used.append(couple[1])

                else:
                    # print("Les touches ne sont que des alphabets en majuscule !")
                    return 1
            else:
                # print("Les touches échangées doivent être écrite sous la forme 'AB CD' !")
                return 1

        return 0

    # Permet de réniatialiser le tableau de connexion
    def reset(self):
        self.connect = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    def chiffrement(self, b):
        c1 = (ord(b))
        if 65 <= c1 <= 90:
            # Récuperation de l'indice de table
            c1 = c1 - 65
        return self.connect[c1]
