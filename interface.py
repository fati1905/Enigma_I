# Pour lancer l'application, veuillez lancer ce fichier 
# Importer des liberairies de Python
import threading
import tkinter
import webbrowser

import customtkinter
from functools import partial
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox

# Nous importons aussi le fichier "machine" qui contient les fonctions gérant les réglages de la machine
import machine

# ---------------------- Variables globales -----------------------------------

# Cette liste permet d'afficher le clavier en "azerty"
alphabets = ['A', 'Z', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'Q', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'W',
             'X', 'C', 'V', 'B', 'N']
listofbuttons = []

# Listes des choix des rotors à afficher dans les figures graphiques
choices_rotor1 = ["I", "V", "IV"]
choices_rotor2 = ["II", "V", "IV"]
choices_rotor3 = ["III", "V", "IV"]

# Liste pour savoir la position des rotors dans l'application
pos = []

# Une chaîne de caractères contenant le texte saisi par l'utilisateur (avant le chiffrement)
textEnter = None


# ----------------------------------- Fonctions ---------------------------------------------------------

# ************ Fonctions de l'attaque **************
# Cette fonction prend en paramètre :
# des : Dossier pour générer des fichiers, fileattaque : Le fichier à décrypter, lock : mutex
# condition : La variable de condition, progressbarWindow : La fenêtre qui affiche les résultats de l'attaque

# Cette fonction permet de lancer l'attaque
def attack(des, fileattaque, lock, condition, progressbarWindow):
    # Lancer l'attaque puis récupérer les solutions
    Res = machine.attaque_1(des, fileattaque, lock, condition)

    # Supprimer la barre de progression et le label de la fenêtre pour afficher les résultats de l'attaque
    progressbarWindow.progress_bar.destroy()
    progressbarWindow.label.destroy()

    # On appelle la méthode "results" de la classe toplevel_attack
    progressbarWindow.results(Res)
    # Changer le nom de la fenêtre "Solutions de l'attaque sur les rotors"
    progressbarWindow.title("Solutions de l'attaque sur les rotors")


# ************** Tableau de connexion ****************
# Cette fonction prend en paramètre event : Événement.
# Elle permet de récupérer les valeurs du tableau de connexion.
# Elle change la couleur de bordure en rouge quand l'utilisateur à entrer un mauvais caractère
def get_plugboard_connections(event):

    # On rénitialise le réglage du tableau de connexion lorsqu'on a le focus dessus
    machine.tab_de_connexion_O.reset()

    # On récupère la saisie de l'utilisateur dans l'entrée
    user_input = window.entry_plugboard.get()
    user_input = user_input.strip()

    # Couper l'entrée de l'utilisateur par les espaces : "AB CG LKM" devient une liste de [AB]-->[CG]-->[LKM]
    list_of_user_input = user_input.split()

    # Teste que si l'entrée de l'utilisateur ne contient pas de contradictions ou de mauvais caractères
    if machine.tab_de_connexion_O.echange(list_of_user_input) == 1:
        # Il y a une erreur : On change la couleur de la bordure en rouge
        window.entry_plugboard.configure(border_color="red")
    else:
        # Il n'y a aucune erreur : La couleur de la bordure reste la même
        window.entry_plugboard.configure(border_color="#9b9ba3")

        # Supprimer l'ancien contenu de la liste de connexion pour le mettre à jour
        machine.list_connexion.clear()

        # mettre le nouveau contenu dans la liste de tableau de connexion
        for connection in list_of_user_input:
            machine.list_connexion.append(connection)

# **************** Événements dans la barre de menu ****************************************
# Cette méthode permet de renvoyer l'utilisateur vers la page github pour la documentation
def open_link():
    webbrowser.open_new("https://github.com/fati1905/Enigma-simulator")


# ***************** Événements sur le clavier ***************************
# alpha : La lettre récupérerée, textbox : Zone d'affichage de texte chiffré
# La fonction permet de récupérer la lettre saisie par l'utilisateur depuis le clavier
def getthecurrentLetter(alpha, textbox):
    global textEnter

    # Afficher la lettre dans le rectangle contenant le texte avant le chiffrement
    window.entry_text.insert(tkinter.END, alpha)

    # Récupérer tous le texte entré depuis le début
    textEnter = window.entry_text.get("0.0", "end")

    # On enlève le \n
    textEnter = textEnter[:-1]

    # Nous allons régler la machine sur les paramètres (au cas de changement) avant le chiffrement
    machine.regler()

    # On chiffre le caractère entré, puis on récupère le caractère de sortie
    alpha = machine.chiffrer(alpha)

    # On met à jour les positions des rotors affichées (A chaque chiffrement d'un caractère, ils avancent)
    window.entry_r1.delete("0", 'end')
    window.entry_r1.insert("0", machine.start_pos[0])
    window.entry_r2.delete("0", 'end')
    window.entry_r2.insert("0", machine.start_pos[1])
    window.entry_r3.delete("0", 'end')
    window.entry_r3.insert("0", machine.start_pos[2])

    # Nous mettons la couleur de la bordure du bouton correspondant à la lettre chiffré en jaune
    for i in range(0, len(listofbuttons)):
        if listofbuttons[i].cget("border_color") == "#EBC31E":
            listofbuttons[i].configure(border_color="#dedee3")
        if listofbuttons[i].cget("text") == alpha:
            listofbuttons[i].configure(border_color="#EBC31E")

    # On ajoute le caractère chiffré dans la zone du texte chiffré
    textbox.insert(tkinter.END, alpha)


# Remettre la couleur du dernier bouton en jaune à la couleur normale
def event_textbox(event):
    for i in range(0, len(listofbuttons)):
        listofbuttons[i].configure(border_color="#dedee3")


# *********************** Événement sur le textenter : Pour l'utilisateur qui écrit depuis son clavier *****************
# Cette fonction permet de récupérer le texte entré par l'utilisateur depuis son propre clavier
# et agir en conséquence en fonction de la touche saisie
# Par exemple : Effacer le chiffré correspondant au lisible effacé par un backspace
#               Chiffrer une lettre saisie et l'ajouter dans le cadre du texte chiffré
def retrieve_text_entry(event):
    global textEnter, pos

    # On cherche ici la position du pointeur dans le texte, c'est à dire que l'on regarde où la touche saisie a été saisie dans le cadre
    ct = tempText = window.entry_text.get("0.0", "end")
    tempText = tempText[:-1]
    pos = window.entry_text.index('insert')
    tabPos = pos.split(".")

    h = int(tabPos[0])
    l = int(tabPos[1])

    cpt = 0
    # on cherche la position dans la chaine
    while h > 1:
        if tempText[cpt] == "\n":
            h -= 1
        cpt += 1

    # L'entier val obtenu ici correspond à l'emplacement du pointeur de l'utilisateur dans le cadre de saisie du texte en clair
    val = cpt + l

    # On sauvegarde la valeur du texte avant suppression par un backspace
    aTextEnter = textEnter

    # On récupère la valeur de la touche saisie
    inserted_text = event.keysym

    # On cherche a obtenir (si la touche saisie n'est pas un BackSpace) la chaîne de caractère complète du cadre de la partie du message non chiffré
    if inserted_text != "BackSpace":
        textEnter = window.entry_text.get("0.0", "end")
        # On enlève le \n
        textEnter = textEnter[:-1]

    # Si on saisit une touche en milieu de chaîne
    if val + 1 != len(ct):
        # On supprime un caractère suite à un backspace uniquement si celui-ci n'est pas une lettre majuscule
        if inserted_text == "BackSpace":
            c = aTextEnter[val]
            if 64 < ord(c) < 91:
                window.entry_text.delete("0.0", "end")
                window.entry_text.insert("end", aTextEnter)

        else:
            # On ajoute le caractère saisi en bout de chaîne
            if len(inserted_text) == 1 and 64 < ord(inserted_text) < 91:
                window.entry_text.delete("0.0", "end")
                ttmp = list(textEnter)
                del ttmp[val - 1]
                ttmp_c = "".join(ttmp)
                window.entry_text.insert("end", ttmp_c)

    # Si on saisit une touche en bout de chaîne
    else:
        # Si c'est une lettre en majuscule, on l'a chiffre et l'affiche dans le cadre correspondant avec le reste du message chiffré
        if len(inserted_text) == 1:
            if 64 < ord(inserted_text) < 91:
                machine.regler()
                alpha = machine.chiffrer(inserted_text)
                window.entry_r1.delete("0", 'end')
                window.entry_r1.insert("0", machine.start_pos[0])
                window.entry_r2.delete("0", 'end')
                window.entry_r2.insert("0", machine.start_pos[1])
                window.entry_r3.delete("0", 'end')
                window.entry_r3.insert("0", machine.start_pos[2])
                window.encrypted_text_zone.insert(tkinter.END, alpha)
        else:
            # Si on backspace et on efface un caractère entre 65 et 90 on efface le chiffré correspodnant à ce carractère "backspacé"
            if inserted_text == "BackSpace":
                if len(textEnter) != 0:
                    text = textEnter
                    textEnter = text[:-1]
                    carac = text[len(text) - 1]
                    if 64 < ord(carac) < 91:
                        machine.start_pos = machine.rotor_O.rotationInverse()
                        window.entry_r1.delete("0", 'end')
                        window.entry_r1.insert("0", machine.start_pos[0])
                        window.entry_r2.delete("0", 'end')
                        window.entry_r2.insert("0", machine.start_pos[1])
                        window.entry_r3.delete("0", 'end')
                        window.entry_r3.insert("0", machine.start_pos[2])

                        window.encrypted_text_zone.delete("end-2c", "end-1c")


# Cette fonction permet après un coller dans le message lissible de le faire correspondre correctement dans la chaîne du message chiffré
def control_v(event):
    global pos

    # On cherche ici la position du pointeur dans le texte, c'est à dire que l'on regarde où la touche saisie a été saisie dans le cadre
    tempText = window.entry_text.get("0.0", "end")
    tempText = tempText[:-1]
    pos = window.entry_text.index('insert')
    tabPos = pos.split(".")

    h = int(tabPos[0])
    l = int(tabPos[1])

    cpt = 0
    # on cherche la position dans la chaine
    while h > 1:
        if tempText[cpt] == "\n":
            h -= 1
        cpt += 1

    # L'entier val obtenu ici correspond à l'emplacement du pointeur de l'utilisateur dans le cadre de saisie du texte en clair
    val = cpt + l

    # On récupère le texte à coller
    acopier = window.clipboard_get()

    # On récupère la nouvelle chaîne à chiffrer
    Achiffrer = tempText[:val] + acopier + tempText[val:]

    # On récupère la chaîne chiffré actuelle
    supp = window.encrypted_text_zone.get("0.0", "end")

    # On cherche ici à faire reculer la position des rotors autant de fois qu'il n'y a de caractère dans la chaîne
    # chiffré
    for i in range(0, len(supp) - 1):
        machine.start_pos = machine.rotor_O.rotationInverse()

    # On supprimer toute la chaîne chiffré
    window.encrypted_text_zone.delete("0.0", "end")

    # On rechiffre un à un tous les caractères présents dans la chaine du message lisible
    for elt in Achiffrer:
        if 64 < ord(elt) < 91:
            machine.regler()
            alpha = machine.chiffrer(elt)
            window.entry_r1.delete("0", 'end')
            window.entry_r1.insert("0", machine.start_pos[0])
            window.entry_r2.delete("0", 'end')
            window.entry_r2.insert("0", machine.start_pos[1])
            window.entry_r3.delete("0", 'end')
            window.entry_r3.insert("0", machine.start_pos[2])

            window.encrypted_text_zone.insert(tkinter.END, alpha)


# ******************** Fonctions pour la fenêtre des réglages **************************************
# Récupère le choix pour le 1er rotor puis mettre à jour les choix des autres rotors
# On ne peut pas choisir le même rotor deux fois
def event_rotor1(choice):
    # On met à jour la liste permettant la configuration d'Enigma du choix du rotor sélectionné

    # On récupère le contenu de la liste permettant la configuration d'Enigma du choix du rotor sélectionné
    lst = machine.wheel_order

    # On change la première option au choix que l'utilisateur vient de faire
    lst[0] = choice
    machine.wheel_order = lst

    # La liste des options
    list_options = ["I", "II", "III", "IV", "V"]

    # Mettre à jour les choix des autres listes pour faire en sorte de ne pas choisir le même rotor plus qu'une seule fois
    # On supprime les contenus des listes qui permettent l'affichage des rotors
    # Par exemple : la liste choices_rotor1 contient que les numéros des rotors qu'on peut utiliser dans l'emplacement 1
    choices_rotor1.clear()
    choices_rotor2.clear()
    choices_rotor3.clear()

    # On met à jour les listes des autres emplacements pour pouvoir choisir les rotors qui étaient sélectionés avant
    # et de ne plus pouvoir choisir le rotor dans l'emplacement 1
    for elem in list_options:
        if elem != window.settings_window.rotor2.get() and elem != window.settings_window.rotor3.get():
            choices_rotor1.append(elem)
        if elem != window.settings_window.rotor3.get() and elem != choice:
            choices_rotor2.append(elem)
        if elem != window.settings_window.rotor2.get() and elem != choice:
            choices_rotor3.append(elem)

    # Réafficher les rotors choisis dans les 3 emplacements
    window.settings_window.rotor1.configure(values=choices_rotor1)
    window.settings_window.rotor2.configure(values=choices_rotor2)
    window.settings_window.rotor3.configure(values=choices_rotor3)


# ---> Même que la fonction d'avant, il faut la revoir pour mieux comprendre
# Récupère le choix pour le 2ᵉ rotors puis mis à jour les choix des autres rotors
# On ne peut pas choisir le même rotor deux fois
def event_rotor2(choice):
    lst = machine.wheel_order
    lst[1] = choice
    machine.wheel_order = lst

    list_options = ["I", "II", "III", "IV", "V"]
    # Mettre à jour les choix des autres listes
    choices_rotor1.clear()
    choices_rotor2.clear()
    choices_rotor3.clear()
    for elem in list_options:
        if elem != window.settings_window.rotor1.get() and elem != window.settings_window.rotor3.get():
            choices_rotor2.append(elem)
        if elem != window.settings_window.rotor1.get() and elem != choice:
            choices_rotor3.append(elem)
        if elem != window.settings_window.rotor3.get() and elem != choice:
            choices_rotor1.append(elem)

    # Update the display
    window.settings_window.rotor1.configure(values=choices_rotor1)
    window.settings_window.rotor2.configure(values=choices_rotor2)
    window.settings_window.rotor3.configure(values=choices_rotor3)


# Récupère le choix pour le 3ᵉ rotors puis mis à jour les choix des autres rotors
# On ne peut pas choisir le même rotor deux fois
def event_rotor3(choice):
    lst = machine.wheel_order
    lst[2] = choice
    machine.wheel_order = lst

    list_options = ["I", "II", "III", "IV", "V"]
    # Mettre à jour les choix des autres listes
    choices_rotor1.clear()
    choices_rotor2.clear()
    choices_rotor3.clear()
    for elem in list_options:
        if elem != window.settings_window.rotor2.get() and elem != window.settings_window.rotor1.get():
            choices_rotor3.append(elem)
        if elem != window.settings_window.rotor1.get() and elem != choice:
            choices_rotor2.append(elem)
        if elem != window.settings_window.rotor2.get() and elem != choice:
            choices_rotor1.append(elem)

    # Update the content of the dropdown
    window.settings_window.rotor1.configure(values=choices_rotor1)
    window.settings_window.rotor2.configure(values=choices_rotor2)
    window.settings_window.rotor3.configure(values=choices_rotor3)


# Mettre à jour la liste de la configuration d'Enigma sur le choix du réflecteur
def event_reflecteur(choice):
    machine.reflecteur = choice


# Récupère le choix d'anneau pour le premier rotor
def event_anneau1(choice):
    # On récupère la liste des choix des anneaux actuels
    lst = machine.anneau

    # On récupère le choix de l'utilisateur
    lst[0] = int(choice)

    # Puis, on la met à jour en changeant la valeur correspondant au premier rotor
    machine.anneau = lst


# Récupère le choix d'anneau pour 2ᵉ rotor
def event_anneau2(choice):
    # On récupère la liste des choix des anneaux actuels
    lst = machine.anneau
    # On récupère le choix de l'utilisateur
    lst[1] = int(choice)
    # Puis, on la met à jour en changeant la valeur correspondant au deuxième rotor
    machine.anneau = lst


# Récupère le choix d'anneau pour le 3ᵉ rotor
def event_anneau3(choice):
    # On récupère la liste des choix des anneaux actuels
    lst = machine.anneau
    # On récupère le choix de l'utilisateur
    lst[2] = int(choice)
    # Puis, on la met à jour en changeant la valeur correspondant au 3ᵉ rotor
    machine.anneau = lst


# ------------------------------------ Classes ----------------------------------------------------------
# Cette classe permet de créer un frame
class create_Frame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)


# Toplevelwindow (fenêtre) pour l'affichage de la barre de progression et les résultats de l'attaque
class toplevelWindow_attack(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):

        # Ouvrir la fenêtre
        super().__init__(*args, **kwargs)
        # L'emplacement en pixel avec la dimension de l'affichage de la fenêtre
        self.geometry("390x300+350+20")
        # Mettre à jour le titre de la fenêtre
        self.title("Attaque")
        # La couleur de la fenêtre est en mode noir
        customtkinter.set_appearance_mode("dark")
        # Le thème de l'application est en bleu foncé
        customtkinter.set_default_color_theme("dark-blue")
        # La fenêtre ne peut pas changer de dimension
        self.resizable(False, False)

        # Ajouter la barre de progression et un label qui affiche la progression de l'attaque en pourcentage
        self.progress_bar = None
        self.progress_value = 0

        # Le label qui afficher le pourcentage de l'attaque
        self.label = customtkinter.CTkLabel(master=self,
                                            text=str(self.progress_value) + "%",
                                            text_color="white",
                                            )
        self.label.place(x=195, y=150)

    # Ajouter la barre de progression
    def addProgressBar(self):
        # On change le nom de la fenêtre
        self.title("Le progrès de l'attaque")
        bar_frame = create_Frame(master=self, fg_color=self['background'])
        bar_frame.place(x=55, y=110)

        # On crée une barre de progression
        self.progress_bar = customtkinter.CTkProgressBar(master=bar_frame,
                                                         progress_color="#083a80",
                                                         width=290,
                                                         height=20,
                                                         border_color="#09082e",
                                                         mode="determinate",
                                                         determinate_speed=1,
                                                         )
        self.progress_bar.pack(padx=5, pady=10)
        self.progress_bar.set(0)

    # Cette méthode permet d'afficher les résultats de l'attaque
    def results(self, res):
        # Ajouter un canvas, si jamais y a beaucoup de résultats, il permet d'afficher une barre de scroll
        canvas = customtkinter.CTkCanvas(self,
                                         bg=self["background"],
                                         height=350,
                                         width=500,
                                         borderwidth=0,
                                         highlightthickness=0)
        canvas.pack(padx=0, pady=0)

        # Ajouter un frame dans le canvas pour afficher les résultats
        frameresult = customtkinter.CTkFrame(master=canvas, fg_color=self["background"])
        frameresult.place(x=70, y=20)

        # Afficher les clés et les anneaux solutions
        countkey = 0
        countring = 0
        for k in res:
            if any(c.isalpha() for c in k):
                # C'est une clé exemple : E K L
                if countkey == 0:
                    label = customtkinter.CTkLabel(master=frameresult,
                                                   text_color="white",
                                                   text="Positions des rotors")
                    label.grid(row=0, column=0, padx=10)
                countkey += 1
                buttonkey = customtkinter.CTkButton(master=frameresult, text=k, state="disabled", width=70, height=33,
                                                    corner_radius=0, fg_color="#222226", border_color="#636366",
                                                    border_width=2, text_color="white")
                buttonkey.grid(row=countkey, column=0, padx=10, pady=2)
            else:
                # C'est un anneau, exemple : 11 26 19
                if countring == 0:
                    label = customtkinter.CTkLabel(master=frameresult,
                                                   text_color="white",
                                                   text="Anneaux possibles")
                    label.grid(row=0, column=1, padx=10)
                countring += 1
                buttonkey = customtkinter.CTkButton(master=frameresult, text=k, state="disabled", width=70, height=33,
                                                    corner_radius=0, fg_color="#222226", border_color="#636366",
                                                    border_width=2, text_color="white")
                buttonkey.grid(row=countring, column=1, padx=10, pady=2)

            # Afficher le scrollbar, quand il y a 7 éléments
            if countkey == 7 or countring == 7:
                scrollbar = customtkinter.CTkScrollbar(canvas, orientation=tkinter.VERTICAL, command=canvas.yview)
                scrollbar.place(x=370, y=0)
                canvas.configure(yscrollcommand=scrollbar.set)


# Le toplevelwindow sert à modifier les réglages de la machine Enigma : Choix des rotors, anneaux, réflecteur
class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kawrgs):
        super().__init__(*args, **kawrgs)
        global choices_rotor1, choices_rotor2, choices_rotor3
        # Ourvir la fenêtre
        # L'emplacement en pixel avec la dimension de l'affichage de la fenêtre
        self.geometry("250x540+770+20")
        # Mettre à jour le titre de la fenêtre
        self.title("Paramètres")
        # La couleur de la fenêtre est en mode noir
        customtkinter.set_appearance_mode("dark")
        # Le thème de l'application est en bleu foncé
        customtkinter.set_default_color_theme("dark-blue")
        # La fenêtre ne peut pas changer de dimension
        self.resizable(False, False)

        # Créer un frame
        self.toplevel_frame1 = create_Frame(master=self, fg_color=self['background'])
        self.toplevel_frame1.pack(padx=1, pady=4)

        # **** Créer les menus déroulants pour les choix des rotors *****
        # On crée d'abord le label pour afficher "Choix des rotors"
        self.label = customtkinter.CTkLabel(master=self.toplevel_frame1, text_color="white", text="Choix des rotors")
        self.label.pack(side=customtkinter.TOP, pady=7)

        # On crée un autre frame pour les combobox
        self.subframe = create_Frame(master=self.toplevel_frame1, fg_color=self['background'])
        self.subframe.pack(side=customtkinter.BOTTOM)

        # Premier combobox pour le rotor 1 / On affiche les valeurs dans la liste choices_rotor1
        self.rotor1 = customtkinter.CTkComboBox(master=self.subframe,
                                                values=choices_rotor1,
                                                fg_color="black",
                                                dropdown_fg_color="black",
                                                dropdown_hover_color="grey",
                                                command=event_rotor1,
                                                width=60
                                                )
        self.rotor1.grid(row=0, column=0, padx=2)
        # On affiche la valeur dans la liste permettant la configuration de la machine de Enigma
        self.rotor1.set(machine.wheel_order[0])

        # Premier combobox pour le rotor 2 / On affiche les valeurs dans la liste choices_rotor2
        self.rotor2 = customtkinter.CTkComboBox(master=self.subframe,
                                                values=choices_rotor2,
                                                fg_color="black",
                                                dropdown_fg_color="black",
                                                dropdown_hover_color="grey",
                                                command=event_rotor2,
                                                width=60
                                                )
        self.rotor2.grid(row=0, column=1, padx=2)
        # On affiche la valeur dans la liste permettant la configuration de la machine de Enigma
        self.rotor2.set(machine.wheel_order[1])

        # Premier combobox pour le rotor 3 / On affiche les valeurs dans la liste choices_rotor3
        self.rotor3 = customtkinter.CTkComboBox(master=self.subframe,
                                                values=choices_rotor3,
                                                fg_color="black",
                                                dropdown_fg_color="black",
                                                dropdown_hover_color="grey",
                                                command=event_rotor3,
                                                width=60
                                                )
        self.rotor3.grid(row=0, column=3, padx=2)
        # On affiche la valeur dans la liste permettant la configuration de la machine de Enigma
        self.rotor3.set(machine.wheel_order[2])

        # **** Créer les menus déroulant pour les anneaux *********
        # Cette listes contient les numéros de 1 à 26, que nous allons afficher dans les menus déroulants
        values = [str(i) for i in range(1, 27)]

        # On crée un frame pour les combobox + le label
        self.toplevel_frame2 = create_Frame(master=self, fg_color=self['background'])
        self.toplevel_frame2.pack(side=customtkinter.TOP, pady=120)

        # On crée un label pour afficher "Anneaux"
        self.label = customtkinter.CTkLabel(master=self.toplevel_frame2, text_color="white", text="Anneaux")
        self.label.pack(side=customtkinter.TOP, pady=7)

        # On crée un sous frame pour les combobox
        self.subframe2 = create_Frame(master=self.toplevel_frame2, fg_color=self['background'])
        self.subframe2.pack(side=customtkinter.BOTTOM)

        self.anneau1 = customtkinter.CTkComboBox(master=self.subframe2,
                                                 values=values,
                                                 fg_color="black",
                                                 dropdown_fg_color="black",
                                                 dropdown_hover_color="grey",
                                                 command=event_anneau1,
                                                 width=60
                                                 )
        self.anneau1.grid(row=0, column=0, padx=2)
        # On affiche l'anneau choisit pour le rotor1 depuis la liste responsable de la configuration de Enigma
        self.anneau1.set(machine.anneau[0])

        self.anneau2 = customtkinter.CTkComboBox(master=self.subframe2,
                                                 values=values,
                                                 fg_color="black",
                                                 dropdown_fg_color="black",
                                                 dropdown_hover_color="grey",
                                                 command=event_anneau2,
                                                 width=60
                                                 )
        self.anneau2.grid(row=0, column=1, padx=2)

        # On affiche l'anneau choisit pour le rotor 2 depuis la liste responsable de la configuration de Enigma
        self.anneau2.set(machine.anneau[1])

        self.anneau3 = customtkinter.CTkComboBox(master=self.subframe2,
                                                 values=values,
                                                 fg_color="black",
                                                 dropdown_fg_color="black",
                                                 dropdown_hover_color="grey",
                                                 command=event_anneau3,
                                                 width=60
                                                 )
        self.anneau3.grid(row=0, column=3, padx=2)

        # On affiche l'anneau choisit pour le rotor 3 depuis la liste responsable de la configuration de Enigma
        self.anneau3.set(machine.anneau[2])

        # ****** Créer un menu déroulant pour le réflecteur ********
        self.toplevel_frame3 = create_Frame(master=self, fg_color=self['background'])
        self.toplevel_frame3.pack(side=customtkinter.BOTTOM, pady=7)

        self.label = customtkinter.CTkLabel(master=self.toplevel_frame3,
                                            text_color="white",
                                            text="Réflecteur"
                                            )
        self.label.pack(side=customtkinter.TOP)

        self.reflector = customtkinter.CTkComboBox(master=self.toplevel_frame3,
                                                   values=["A", "B", "C"],
                                                   fg_color="black",
                                                   dropdown_fg_color="black",
                                                   dropdown_hover_color="gray",
                                                   command=event_reflecteur,
                                                   )
        self.reflector.pack(side=customtkinter.BOTTOM)
        # On affiche le réflecteur choisi
        self.reflector.set(machine.reflecteur)


# ********************** La classe de la fenêtre principale **************************
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # Ouverture de la fenêtre
        # La barre de menu est nulle pour l'instant, mais sera créer après
        self.menu = None
        # La position et les dimensions de la fenêtre
        self.geometry("590x540+20+20")
        self.title("ENIGMA I")
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")
        self.resizable(False, False)

        # Ajout de la barre du menu
        self.addMenuBar()

        self.settings_window = None

        # Gérer l'au-dessus du clavier : L'affichage du texte chiffré + la clé et le tableau de connexion
        self.lamps_keyboard = create_Frame(master=self, height=300)
        self.lamps_keyboard.pack(side=customtkinter.TOP)
        self.lamps_keyboard.bind("<Enter>", event_textbox)

        # ******** Création des éléments de la première partie ********
        # -------------- Création d'un textbox pour l'affichage du texte avant le chiffrement -------------
        self.display = create_Frame(master=self.lamps_keyboard)
        self.display.grid(row=0, column=0, pady=10, padx=10)
        self.entry_text = customtkinter.CTkTextbox(master=self.display,
                                                   width=350,
                                                   height=70,
                                                   border_width=2,
                                                   border_color="#636366",
                                                   fg_color="#222226",
                                                   text_color="white"
                                                   )
        self.entry_text.pack(padx=1)

        # Les événements sur entry_text : Affichage de la lettre saisie par l'utilisateur, Les commandes ctrl+v et ctrl+c
        self.entry_text.bind("<KeyRelease>", retrieve_text_entry)
        self.entry_text.bind("<Control-v>", control_v)
        self.entry_text.bind("<Command-v>", control_v)

        # -------------- Création d'un textbox pour l'affichage du texte chiffré -------------
        self.encrypted_text_zone = customtkinter.CTkTextbox(master=self.display,
                                                            width=350,
                                                            height=70,
                                                            border_width=2,
                                                            border_color="#636366",
                                                            fg_color="#222226",
                                                            text_color="white"
                                                            )
        self.encrypted_text_zone.pack(padx=0)

        # ************* Création d'un frame à droite pour la gestion de la clé et le tableau de connexion *************
        self.settings_frame = create_Frame(self.lamps_keyboard, fg_color="#222226")
        self.settings_frame.grid(row=0, column=1, padx=10, pady=10)

        # --- Partie 1 : Créer les positions des rotors ---
        self.partie_une = create_Frame(master=self.settings_frame, fg_color="#222226")
        self.partie_une.pack(side=customtkinter.TOP)

        self.label_pos_des_rotors = customtkinter.CTkLabel(master=self.partie_une,
                                                           text_color="white",
                                                           text="Positionnement des rotors"
                                                           )
        self.label_pos_des_rotors.pack(padx=2, pady=1)

        self.frame_pos = create_Frame(master=self.partie_une, fg_color="#222226")
        self.frame_pos.pack(padx=1, pady=2)

        self.entry_r1 = customtkinter.CTkEntry(master=self.frame_pos,
                                               placeholder_text="A",
                                               width=10,
                                               height=10,
                                               corner_radius=3,
                                               border_color="#9b9ba3"
                                               )
        self.entry_r1.grid(row=0, column=0, padx=2)

        self.entry_r2 = customtkinter.CTkEntry(master=self.frame_pos,
                                               placeholder_text="A",
                                               width=10,
                                               height=10,
                                               corner_radius=3,
                                               border_color="#9b9ba3"
                                               )
        self.entry_r2.grid(row=0, column=1, padx=2)
        self.entry_r3 = customtkinter.CTkEntry(master=self.frame_pos,
                                               placeholder_text="A",
                                               width=10,
                                               height=10,
                                               corner_radius=3,
                                               border_color="#9b9ba3"
                                               )
        self.entry_r3.grid(row=0, column=2, padx=2)

        # Le contenu par défaut de la clé
        self.entry_r1.insert("0", "A")
        self.entry_r2.insert("0", "A")
        self.entry_r3.insert("0", "A")

        # Récupération de la clé
        self.entry_r1.bind("<KeyRelease>", self.retrieve_pos1)
        self.entry_r2.bind("<KeyRelease>", self.retrieve_pos2)
        self.entry_r3.bind("<KeyRelease>", self.retrieve_pos3)

        pos.clear()

        # Ce frame est fait pour l'esthétique
        self.vide = create_Frame(master=self.settings_frame, fg_color="#222226", height=40)
        self.vide.pack()

        # ------- Partie 2 : Tableau de connexion ---------
        self.partie_deux = create_Frame(master=self.settings_frame, fg_color="#222226")
        self.partie_deux.pack(side=customtkinter.BOTTOM, pady=3)

        # Tableau de connexion
        self.label_plugboard = customtkinter.CTkLabel(master=self.partie_deux,
                                                      text_color="white",
                                                      text="Tableau de connexion"
                                                      )
        self.label_plugboard.pack(padx=0, pady=1)

        # L'entrée pour récupérer les connexions du tableau de connexion
        self.entry_plugboard = customtkinter.CTkEntry(master=self.partie_deux,
                                                      placeholder_text="ex: AB JK LK MP NB TY",
                                                      width=175,
                                                      height=10,
                                                      corner_radius=3,
                                                      border_color="#9b9ba3",
                                                      # font=("InknutAntiqua", 10)
                                                      )
        self.entry_plugboard.pack(padx=3)
        # événement pour récupérer les caractères saisis
        self.entry_plugboard.bind("<KeyRelease>", get_plugboard_connections)

        # Créer une fenêtre pour espacer les deux parties
        # Gérer le clavier
        self.keyboard = create_Frame(master=self, fg_color="#222226")
        self.keyboard.pack(side=customtkinter.BOTTOM)

        # Les botons du premier rang : On appelle la méthode qui les construit
        self.first_row = create_Frame(master=self.keyboard, fg_color="#222226")
        self.keyboard_buttons(0, 10, 3, 7, self.first_row, self.encrypted_text_zone)

        # Création des botons du 2ᵉ rang
        self.second_row = create_Frame(master=self.keyboard, fg_color="#222226")
        self.keyboard_buttons(10, 20, 10, 6, self.second_row, self.encrypted_text_zone)

        # Les botons du 3ᵉ rang
        self.third_row = create_Frame(master=self.keyboard, fg_color="#222226")
        self.keyboard_buttons(20, 26, 20, 7, self.third_row, self.encrypted_text_zone)

    # ****************** Affichage des botons *********************
    # Cette méthode est appelée pour la création des botons
    def keyboard_buttons(self, alphastart, alphaend, padding_x, padding_y, subframe, encrypted_text_zone):
        # Ajout du frame de chaque rand
        subframe.pack(padx=padding_x, pady=padding_y)

        # Ajout des botons
        col = 0
        for i in range(alphastart, alphaend):
            action_after_button_press = partial(getthecurrentLetter, alphabets[i], encrypted_text_zone)
            listofbuttons.append(customtkinter.CTkButton(master=subframe,
                                                         width=40,
                                                         height=40,
                                                         corner_radius=15,
                                                         fg_color="black",
                                                         border_color="#dedee3",
                                                         border_width=2,
                                                         hover_color="#09082e",
                                                         text_color="white",
                                                         text=alphabets[i],
                                                         hover=True,
                                                         command=action_after_button_press
                                                         ))

            listofbuttons[i].grid(row=0, column=col, pady=10, padx=5)
            col += 1

    # ****************** Affichage de la barre de menu *********************
    # Cette méthode permet la gestion des éléments de la barre de menu
    def addMenuBar(self):
        # On instancie la barre de menu, puis on l'ajoute à la fenêtre
        self.menu = tkinter.Menu(self, background=self['background'], fg='white')
        self.config(menu=self.menu)

        # On cée le sous menu de Chiffrement/Déchiffrement
        submenu1 = tkinter.Menu(self.menu, tearoff=0, background=self['background'], fg='white')
        self.menu.add_cascade(label="Chiffrement/Déchiffrement", menu=submenu1)

        # Puis, on lui ajoute les autres choix (Générer un fichier type, chiffrer un fichier après amélioration, etc)
        submenu1.add_command(label="Générer un fichier type", font=("", 10), command=self.generationFichier)
        submenu1.add_command(label="Chiffrer un fichier après amélioration", font=("", 10),
                             command=self.chiffrementAmeliore)
        submenu1.add_command(label="Déchiffrer un fichier après amélioration", font=("", 10),
                             command=self.dechiffrementAmeliore)
        submenu1.add_command(label="Chiffrer un fichier avant amélioration", font=("", 10),
                             command=self.chiffrementNonAmeliore)
        submenu1.add_command(label="Déchiffrer un fichier avant amélioration", font=("", 10),
                             command=self.dechiffrementNonAmeliore)

        # Créer le sous-menu pour "Attaque"
        submenu2 = tkinter.Menu(self.menu, tearoff=0, background=self['background'], fg='white')
        self.menu.add_cascade(label="Attaque", menu=submenu2)

        # On lui ajoute les choix suivants :
        submenu2.add_command(label="Génération de fichiers interceptées", font=("", 10),
                             command=self.generationFichierInterceptes)
        submenu2.add_command(label="Représentation de l'Orbite", font=("", 10), command=self.graphe_)
        submenu2.add_command(label="Attaque sur rotors et anneaux", font=("", 10), command=self.attaque1)
        submenu2.add_command(label="Attaque sur tableau de connexion", font=("", 10), command=self.attaque2)

        # On crée le sous menu pour ouvrir la fenêtre des réglages
        submenu3 = tkinter.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Réglages", menu=submenu3)
        # On est obligé d'ajouter "ouvrir" pour ouvrir la fenêtre
        submenu3.add_command(label="Ouvrir", font=("", 10), command=self.open_settings_tab)

        # Ceci permet de ne pas dissocier le menu de la fenêtre
        submenu4 = tkinter.Menu(self.menu, tearoff=0)

        # On crée le dernier sous menu pour rediriger l'utilisateur vers la page de github pour faire consulter la doc
        self.menu.add_cascade(label="Aide", menu=submenu4)
        submenu4.add_command(label="Aller sur github", font=("", 10), command=open_link)

    # ****************** Ouverture la fenêtre des réglage (événement) *********************
    # Cette méthode permet d'ouvrir la fenêtre des réglages
    def open_settings_tab(self):
        if self.settings_window is None or not self.settings_window.winfo_exists():
            # Si la fenêtre n'est pas créée, on l'instancie
            self.settings_window = ToplevelWindow(self)

        else:
            # Si la fenêtre est déjà ouverte, on met un focus
            self.settings_window.focus()

    # ****************** Récupérer la position des rotors (événement) *********************
    # Les 3 méthodes en bas permettent de récupérer l'entrée de l'utilisateur lors de la saisie de la positions des rotors
    def retrieve_pos1(self, event):
        # On récupère le caractère saisi
        pos1 = self.entry_r1.get()
        # On transforme la saisie à une liste pour vérifier les fautes
        pos1_list = list(pos1)

        # Gestion d'erreur : Si l'utilisateur a mis plus d'un caractère, on signale l'erreur
        if len(pos1_list) != 1:
            # Il y a une erreur --> On change la couleur de la bordure en rouge
            self.entry_r1.configure(border_color="red")
        else:
            # On teste si le caractère saisi est un alphabet en majuscule
            if 64 < ord(pos1_list[0]) < 91:
                # Il n'y a aucune erreur --> La couleur reste la même que celle du début
                self.entry_r1.configure(border_color="#9b9ba3")
                # On met la liste responsable de la configuration de Enigma à jour
                machine.start_pos[0] = pos1_list[0]
            else:
                # Si l'utilisateur a saisi un mauvais caractère, la bordure devient rouge
                self.entry_r1.configure(border_color="red")

    # Le même que pour la méthode retrieve_pos1
    def retrieve_pos2(self, event):
        pos2 = self.entry_r2.get()

        pos2_list = list(pos2)

        if len(pos2_list) != 1:
            self.entry_r2.configure(border_color="red")
        else:
            if 64 < ord(pos2_list[0]) < 91:
                self.entry_r2.configure(border_color="#9b9ba3")
                machine.start_pos[1] = pos2_list[0]
            else:
                self.entry_r2.configure(border_color="red")

    # Le même que pour la méthode retrieve_pos1
    def retrieve_pos3(self, event):
        pos3 = self.entry_r3.get()

        pos3_list = list(pos3)

        if len(pos3_list) != 1:
            self.entry_r3.configure(border_color="red")
        else:
            if 64 < ord(pos3_list[0]) < 91:
                self.entry_r3.configure(border_color="#9b9ba3")
                machine.start_pos[2] = pos3_list[0]
            else:
                self.entry_r3.configure(border_color="red")

    # ****************** Attaque (événement) *********************
    #   options pour générer les fichiers de l'attaque
    def generationFichier(self):
        filename1 = filedialog.askopenfilename(title="Sélectionner le fichier à chiffrer",
                                               filetypes=(('text files', '*.txt'),('text files', '*.enigmaI')))
        # Si l'utilisateur n'a pas choisi le fichier à chiffrer
        if not filename1:
            # Afficher un warning
            tkinter.messagebox.showwarning("Erreur",
                                           " Vous devez choisir un fichier contenant le message à chiffrer")
            # Arrêter l'action
            return

        machine.generation_Fichier(filename1)

    #   changement de la clef à afficher
    def chiffrementAmeliore(self):
        # Open a file
        filename1 = filedialog.askopenfilename(title="Sélectionner le fichier à chiffrer",
                                               filetypes=(('text files', '*.txt'),('text files', '*.enigmaI')))
        # Si l'utilisateur n'a pas choisi le fichier à chiffrer
        if not filename1:
            # Afficher un warning
            tkinter.messagebox.showwarning("Erreur",
                                           " Vous devez choisir un fichier contenant le message à chiffrer")
            # Arrêter l'action
            return

        filename2 = filedialog.askopenfilename(title="Sélectionner le fichier de destination",
                                               filetypes=(('text files', '*.txt'),('text files', '*.enigmaI')))

        # Si l'utilisateur n'a pas choisi le fichier de destination
        if not filename2:
            # Afficher un warning
            tkinter.messagebox.showwarning("Erreur",
                                           " Vous devez choisir un fichier de destination")
            # Arrêter l'action
            return

        machine.chiffrement_ameliore(filename1, filename2)
        pos1 = self.entry_r1.get()
        pos2 = self.entry_r2.get()
        pos3 = self.entry_r3.get()
        machine.start_pos[0] = pos1
        machine.start_pos[1] = pos2
        machine.start_pos[2] = pos3

    def dechiffrementAmeliore(self):
        # Open a file
        filename1 = filedialog.askopenfilename(title="Sélectionner le fichier à déchiffrer",
                                               filetypes=(('text files', '*.txt'),('text files', '*.enigmaI')))
        # Si l'utilisateur n'a pas choisi le fichier à déchiffrer
        if not filename1:
            # Afficher un warning
            tkinter.messagebox.showwarning("Erreur",
                                           "Vous devez choisir un fichier contenant le message à déchiffrer")
            # Arrêter l'action
            return

        filename2 = filedialog.askopenfilename(title="Sélectionner le fichier de destination",
                                               filetypes=(('text files', '*.txt'),('text files', '*.enigmaI')))

        # Si l'utilisateur n'a pas choisi le fichier de destination
        if not filename2:
            # Afficher un warning
            tkinter.messagebox.showwarning("Erreur",
                                           " Vous devez choisir un fichier de destination")
            # Arrêter l'action
            return

        machine.dechiffrement_ameliore(filename1, filename2)
        pos1 = self.entry_r1.get()
        pos2 = self.entry_r2.get()
        pos3 = self.entry_r3.get()
        machine.start_pos[0] = pos1
        machine.start_pos[1] = pos2
        machine.start_pos[2] = pos3

    def chiffrementNonAmeliore(self):
        # Open a file
        filename1 = filedialog.askopenfilename(title="Sélectionner le fichier à chiffrer",
                                               filetypes=(('text files', '*.txt'),('text files', '*.enigmaI')))
        # Si l'utilisateur n'a pas choisi le fichier à chiffrer
        if not filename1:
            # Afficher un warning
            tkinter.messagebox.showwarning("Erreur",
                                           "Vous devez choisir un fichier contenant le message à chiffrer")
            # Arrêter l'action
            return

        filename2 = filedialog.askopenfilename(title="Sélectionner le fichier de destination",
                                               filetypes=(('text files', '*.txt'),('text files', '*.enigmaI')))

        # Si l'utilisateur n'a pas choisi le fichier de destination
        if not filename2:
            # Afficher un warning
            tkinter.messagebox.showwarning("Erreur",
                                           " Vous devez choisir un fichier pour y placer le message chiffré")
            # Arrêter l'action
            return

        machine.chiffrement_non_ameliore(filename1, filename2)
        pos1 = self.entry_r1.get()
        pos2 = self.entry_r2.get()
        pos3 = self.entry_r3.get()
        machine.start_pos[0] = pos1
        machine.start_pos[1] = pos2
        machine.start_pos[2] = pos3

    # @ARECOMMNTER
    def dechiffrementNonAmeliore(self):
        # Open a file
        filename1 = filedialog.askopenfilename(title="Sélectionner le fichier à déchiffrer",
                                               filetypes=(('text files', '*.txt'),('text files', '*.enigmaI')))

        # Si l'utilisateur n'a pas choisi le fichier à déchiffrer
        if not filename1:
            # Afficher un warning
            tkinter.messagebox.showwarning("Erreur",
                                           " Vous devez choisir un fichier pour le déchiffrer")
            # Arrêter l'action
            return

        filename2 = filedialog.askopenfilename(title="Sélectionner le fichier de destination",
                                               filetypes=(('text files', '*.txt'),('text files', '*.enigmaI')))

        # Si l'utilisateur n'a pas choisi le fichier de destination
        if not filename2:
            # Afficher un warning
            tkinter.messagebox.showwarning("Erreur",
                                           " Vous devez choisir un fichier pour y placer le message déchiffré")
            # Arrêter l'action
            return

        machine.dechiffrement_non_ameliore(filename1, filename2)
        pos1 = self.entry_r1.get()
        pos2 = self.entry_r2.get()
        pos3 = self.entry_r3.get()
        machine.start_pos[0] = pos1
        machine.start_pos[1] = pos2
        machine.start_pos[2] = pos3

    # @ARECOMMNTER
    def dechiffrementNonAmeliore(self):
        # Open a file
        filename1 = filedialog.askopenfilename(title="Sélectionner le fichier à déchiffrer",
                                               filetypes=(('text files', '*.txt'),('text files', '*.enigmaI')))
        # Si l'utilisateur n'a pas choisi le fichier à déchiffrer
        if not filename1:
            # Afficher un warning
            tkinter.messagebox.showwarning("Erreur",
                                           " Vous devez choisir un fichier pour le déchiffrer")
            # Arrêter l'action
            return

        filename2 = filedialog.askopenfilename(title="Sélectionner le fichier de destination",
                                               filetypes=(('text files', '*.txt'),('text files', '*.enigmaI')))

        # Si l'utilisateur n'a pas choisi le fichier de destination
        if not filename2:
            # Afficher un warning
            tkinter.messagebox.showwarning("Erreur",
                                           " Vous devez choisir un fichier pour y placer le message déchiffré")
            # Arrêter l'action
            return

        machine.dechiffrement_non_ameliore(filename1, filename2)
        pos1 = self.entry_r1.get()
        pos2 = self.entry_r2.get()
        pos3 = self.entry_r3.get()
        machine.start_pos[0] = pos1
        machine.start_pos[1] = pos2
        machine.start_pos[2] = pos3

    # Géneration de fichier intercepté pour l'attaque
    def generationFichierInterceptes(self):

        des = filedialog.askdirectory(
            title="Sélectionner le dossier dans lesquels les fichiers interceptés s'enregistreront")

        # Si l'utilisateur n'a pas choisi le dossier
        if not des:
            # Afficher un warning
            tkinter.messagebox.showwarning("Erreur",
                                           " Vous devez choisir un dossier")
            # Arrêter l'action
            return
        flag = 0
        while flag == 0:
            key = simpledialog.askstring("Saisir la clé", "Clé utilisé de la forme 'ABC' (attaque polonaise)")
            if len(key) == 3:
                cpt = 0
                for i in range(0, len(key)):
                    if 65 <= ord(key[i]) <= 90:
                        cpt += 1
                if cpt == 3:
                    flag = 1

        machine.generation_fichier_interceptes(key, des)
        pos1 = self.entry_r1.get()
        pos2 = self.entry_r2.get()
        pos3 = self.entry_r3.get()
        machine.start_pos[0] = pos1
        machine.start_pos[1] = pos2
        machine.start_pos[2] = pos3

    # Cette méthode permet de faire l'attaque
    def attaque1(self):
        # L'utilisateur choisit le dossier des interceptions
        des = filedialog.askdirectory(
            title="Sélectionner le dossier dans lesquels les fichiers interceptés s'y trouvent")

        # Si l'utilisateur n'a pas choisi un dossier des interceptions
        if not des:
            # Afficher un warning
            tkinter.messagebox.showwarning("Erreur",
                                           " Vous dever choisir le dossier des interceptions du jour")
            # Arrêter l'action
            return

        fileattaque = filedialog.askopenfilename(title="Fichier à attaquer", filetypes=(('text files', '*.txt'),('text files', '*.enigmaI')))

        # Si l'utilisateur n'a pas choisi le fichier de l'attaque
        if not fileattaque:
            # Afficher un warning
            tkinter.messagebox.showwarning("Erreur",
                                           " Vous dever choisir un fichier contenant le message à attaquer")
            # Arrêter l'action
            return

        # Création de la fenête avec la barre de progression
        progressbarWindow = toplevelWindow_attack(self)
        progressbarWindow.addProgressBar()

        # Création d'un mutex et une variable de condition pour la gestion des threads
        lock = threading.Lock()
        condition = threading.Condition(lock)

        # Création et lancement des threads pour l'attaque et la barre de progression
        attack_thread = threading.Thread(target=attack, args=(des, fileattaque, lock, condition, progressbarWindow))
        thread_progress = threading.Thread(target=self.progress, args=(
            progressbarWindow.progress_bar, progressbarWindow.progress_value, progressbarWindow, attack_thread, lock,
            condition))

        # Les threads commencent
        attack_thread.start()
        thread_progress.start()

    # Cette méthode permet la progression de la barre de progression quand l'attaque est mise en route
    def progress(self, bar, pourcent, progressbarWindow, thread_attack, lock, condition):

        # On acquiert le mutex
        with lock:
            # Tant que le thread qui lance l'attaque n'a pas commencé on attend
            while not thread_attack.is_alive():
                condition.wait()

        # Tant que le thread qui fait l'attaque est vivant
        while thread_attack.is_alive():
            # On acquiert le mutex
            lock.acquire()

            # la barre de progression avance
            # 352 vient du calcul suffisant pour faire l'attaque, en effet progress_var est un compteur qui compte l'avancement de l'attaque
            if machine.progress_var >= 352:
                # On réveille l'autre thread
                condition.notify()
                # Puis, on avance la barre de progression d'une étape
                bar.step()
                pourcent += 1
                # On met à jour le label aussi
                progressbarWindow.label.configure(text=(str(int(bar.get() * 100)) + " %"))
                bar.progress_value = int(bar.get() * 100)
                machine.progress_var = 0

            # Tant que l'attaque n'a pas beaucoup avancé et le thread est vivant, on attend
            while machine.progress_var < 352 and thread_attack.is_alive():
                condition.wait()
            lock.release()

        # A la fin, on met la barre à 100%
        bar.set(100)

    # Cette méthode effectue l'attaque sur le tableau de connexion
    def attaque2(self):
        # L'utilisateur choisit un fichier contenant le texte du message après attaque 1
        fileattaque = filedialog.askopenfilename(title="Fichier avec le message après attaque sur les rotors",
                                                 filetypes=(('text files', '*.txt'),('text files', '*.enigmaI')))

        # Si l'utilisateur n'a pas choisi le fichier de l'attaque
        if not fileattaque:
            # Afficher un warning
            tkinter.messagebox.showwarning("Erreur",
                                           " Vous dever choisir un fichier contenant le message à attaquer")
            # Arrêter l'action
            return
        # On effectue une attaque sur le fichier, puis on récupère les solutions de l'attaque
        Res = machine.attaque_2(fileattaque)

        # Ouvrir la fenêtre toplevel window pour afficher les résultats de l'attaque
        toplelevelWind = customtkinter.CTkToplevel(self)
        # On spécifie les dimensions plus la taille de la fenêtre
        toplelevelWind.geometry("370x270+350+20")
        # On ajoute un titre à la fenêtre
        toplelevelWind.title("Résultat de l'attaque")
        # On choisit le thème de la fenêtre
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")
        # La fenêtre ne peut pas changer les dimensions
        toplelevelWind.resizable(False, False)

        # On ajoute un label pour dire que c'est les résultat de l'attaque sur le tableau de connexion
        label = customtkinter.CTkLabel(master=toplelevelWind, text_color="white",
                                       text="Résultat de l'attaque sur le tableau de "
                                            "connexion :")
        label.pack(padx=5, pady=30)

        # On récupère les résultats de l'attaque, puis on les transforme sous une chaine de caractères
        textOfResult = ""
        for i in range(0, int(len(Res)), 2):
            textOfResult = textOfResult + Res[i] + Res[i + 1] + " "

        # On affiche les résultats dans un bouton
        button = customtkinter.CTkButton(master=toplelevelWind, width=170, height=28, corner_radius=None,
                                         state="disabled",
                                         fg_color="#222226", border_color="#636366",
                                         border_width=2, text_color="white", text=textOfResult)
        button.pack(padx=20, pady=2)

        # Les positions des rotors changent avec l'attaque, nous allons remettre celles avant l'attaque
        pos1 = self.entry_r1.get()
        pos2 = self.entry_r2.get()
        pos3 = self.entry_r3.get()
        machine.start_pos[0] = pos1
        machine.start_pos[1] = pos2
        machine.start_pos[2] = pos3

    # Cette méthode permet d'avoir le graphe de l'attaque
    def graphe_(self):
        machine.graphe()


# Créer de la fenêtre
window = App()
# Mise en route de la fenêtre
window.mainloop()
