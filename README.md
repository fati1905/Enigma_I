# Enigma-simulator
<h3> Introduction :</h3> 

L'application Enigma est un logiciel qui permet de simuler le fonctionnement de la machine ENIGMA I, qui a servi le siècle dernier notamment pendant la Seconde Guerre mondiale pour chiffrer ou déchiffrer les échanges entre les commandants et les soldats Nazis. Notre application est aussi équipée pour attaquer un message, c'est-à-dire qu'elle permet de trouver la clé d'un message chiffré.
</br>
<h3> Prérequis pour démarrer l'application :</h3>

Pour lancer l'application sur le terminal, l'utilisateur doit avoir Python 3.11 sur sa machine. Si ce n'est pas le cas, il est téléchargeable depuis le site https://www.python.org/downloads/. L'application ne pourra se lancer qu'avec cette version de Python. Après l'installation du python, il faudra installer aussi certains packages :


- Customtkinter : Gestion de l'interface graphique.
</br><i> pip3 install customtkinter (À installer depuis le terminal)</i> 

- Networkx : Gestion et manipulation des graphes.
</br><i> pip3 install networkx (À installer depuis le terminal)</i>

<h2> Comment régler la machine ? </h2>

Il faut tout d'abord ouvrir l'application depuis le terminal : <i>python3 interface.py</i>

![Screenshot 2023-03-13 175502](https://user-images.githubusercontent.com/81489719/224773960-f28bf19e-803b-4e72-aea3-b053301b3b95.png)

<b>1. Choisir l'ordre des rotors :</b> <p>Il faut ouvrir l'application puis cliquer sur "Réglage" dans la barre de menu en haut de la fenêtre. Ensuite, cliquer sur ouvrir.</p>
![Screenshot 2023-03-13 175352](https://user-images.githubusercontent.com/81489719/224772752-c4c615c1-8899-411e-9766-cb263d4eb95e.png)
<p>La fenêtre à droite qui s'ouvre contient les menus déroulants pour choisir les rotors en dessous du "Choix des rotors", vous ne pouvez pas utiliser le même rotor plus qu'une fois. Si le rotor était déjà sélectionné dans un autre emplacement, désélectionnez-le pour le choisir dans l'emplacement que vous voulez.</p>

<b>2. Choisir l'anneau :</b> <p>Suivez les mêmes étapes décrites dans (1) pour ouvrir la fenêtre du réglage de la machine. Vous avez à votre disposition des menus déroulant sous le champs "Anneau" au milieu de la fenêtre. Le menu déroulant à gauche correspond à l'anneau du premier rotor (celui à gauche), celui du milieu correspond à l'anneau du deuxième rotor et ainsi de suite. Les anneaux sont des numéros de 1 à 26.</p>
![2](https://user-images.githubusercontent.com/81489719/224721523-9c0f1141-0864-4457-98cc-de03a4f4ed75.png)

<b>3. Choix du réflecteur :</b><p> Suivez les mêmes étapes décrites dans (1) pour ouvrir la fenêtre du réglage de la machine Enigma. Vous avez à votre disposition un menu déroulant pour choisir le réflecteur en bas de la fenêtre sous le champs "Réflecteur". Vous avez 3 options : A, B et C.
![3](https://user-images.githubusercontent.com/81489719/224721799-cb2b5d08-c296-4129-8a63-d1444cd3608b.png)

<b>4. Tableau de connexion :</b><p> Ouvrez l'application, vous avez un champs en haut à droite pour insérer les connexions en pairs séparés d'un espace.</p>
![Screenshot 2023-03-13 145520](https://user-images.githubusercontent.com/81489719/224723288-c23f6400-e651-4e55-a05b-fb4afac9e753.png)

<p>Par exemple pour connecter A et B, et connecter C et D vous allez insérer : AB CD. Vous ne pouvez utiliser que des lettres majuscules sans les répeter plusieurs fois (ex : AB GB). Si votre saisie est incorrecte, le bord du champs devient rouge.</p>

<b>6. Positionner les rotors :</b><p> Ouvrez l'application, vous pouvez voir trois champs sous "Positionnement des rotors". Le premier champs correspond à la position du premier rotor, celui du milieu correspond à la position du deuxième rotor et ainsi de suite. Les champs acceptent comme valeur un alphabet en majuscule qui correspond à la position du rotor. Si votre saisie est fausse (plusieurs caractères, un caractère qui n'est pas une une lettre de l'alphabet en majuscule), la couleur de la bordure devient rouge.</p>
![6](https://user-images.githubusercontent.com/81489719/224724358-4d7f13ec-2f5f-465d-bdc2-7b5e651b9611.png)

<h2> Comment chiffrer/déchiffrer un message ? </h2>

<p>Avant de commencez le chiffrement ou le déchiffrement, retenez que l'action du chiffrement et la même que l'action du déchiffrement. C'est-à-dire, si vous allez chiffrer ou déchiffrer il suffit de régler la machine sur les mêmes réglages puis vous pouvez saisir votre message.</p>

<b>1. Depuis le clavier de la machine :</b><p> Ouvrez l'application, vous avez en bas un clavier des lettres majuscules. Tapez votre message depuis ce clavier. La lettre colorée en jaune représente la lettre chiffrée. En haut à droite, vous avez deux rectangles. Le premier en haut affiche le texte que vous saisissez avant le chiffrement/Déchiffrement et le rectangle en bas affiche le texte déchiffré/chiffré.

 <b>2. Depuis le clavier de votre machine :</b><p> En haut à gauche vous avez deux rectangles. Cliquez sur celui le plus haut, puis écrivez votre message depuis le clavier de votre machine. Ensuite, vous avez en bas le texte chiffré/déchiffré correspondant. Pour chiffrer ou déchiffrer votre message, il faut l'écrire en lettre majuscule sinon le caractère ne sera pas chiffré ou déchiffré.</p>

<p>Le texte inséré dans les deux rectangles peut être copié avec la commande ctrl+c ou collé avec la commande ctrl+v. Attention de ne pas avoir votre clavier en "Maj lock"</p> 

<h2> Comment chiffrer/déchiffrer un fichier ? </h2>

Pour chiffrer ou déchiffrer un fichier, nous utilisons les méthodes suivis pendant le dernier siècle. En effet, durant la seconde guerre mondiale, les soldats disposaient d'une feuille sur laquelle étaient écrite les réglages des jours. C'est-à dire quels rotors choisir et dans quel ordre, ainsi que les anneaux de chaque rotor et les connexions entre les lettres pour tous les jours du mois.

![feuille](https://user-images.githubusercontent.com/81489719/224825850-750027c1-5164-438b-831a-31d76dc2ecfe.jpg)

Vous pouvez écrire votre message lisible ou un message chiffré dans un fichier. Votre fichier devra inclure un entête suivant le format  : "Temps actuel = nombre de parties du message = N° de la parti du message = Nombre de caractères totales = clé".

Pour avoir la clé :

Dans le cas de la méthode "polonaise" (utilisé avant l'amélioration) : elle est composé d'un premier trigramme (le Grundstellung) et un autre trigramme choisie aléatoirement.

Dans le cas de la métode amélioré elle est composé d'un premier trigramme (le Grundstellung) et d'un deuxième trigramme le Spruchschlussel.

Exemple d'entête utilisé : 1054 (Temps actuel) = 1 (Un seul message sur une seule partie) = 1 (La première partie du message) = Nombre de caractères = ABCXWN.

![image](https://user-images.githubusercontent.com/81489719/224827900-0dc9d479-f4ac-49c9-80f7-15b362ff9b9d.png)

Après vous retournez à la ligne, vous choisissez deux caractères aléatoires, suivez du kengruppen qui correspond à vos réglages du jour. Le kengtuppen comme vous le voyez dans l'image des réglages du jour permet de vérfier la date du jour, donc les réglages utilisés.

Après avoir préparé le fichier, vous allez ouvrir l'application puis en haut à droite vous cliquez sur "Chiffrement/Déchiffrement" dans la barre de menu.

![Screenshot 2023-03-13 215729](https://user-images.githubusercontent.com/81489719/224830743-a0dccd7f-0060-4348-a224-e59ebe1e4c29.png)

Soulignons ici que l'attaque ne peut se faire uniquement sur un fichier chiffré par la méthode avant amélioration (méthode polonaise). Pour chiffrer un message pouvant être attaquable il faut donc selectionné "Chiffrer un fichier avant amélioration".

<h2> Comment décrypter un fichier ? </h2>

L'objectif du décryptage d'un fichier est de trouver les réglages de Enigma à partir d'un fichier. Pour cela, vous allez avoir besoin de chiffer un message par l'intermédiaire d'un fichier comme expliqué dans la section "Comment chiffrer/déchiffrer un fichier ?".  

Après avoir créer votre fichier avec le message à décrypter, vous allez ouvrir l'application puis cliquer dans la barre de menu sur "Attaquer" : 

![Screenshot 2023-03-17 164159](https://user-images.githubusercontent.com/81489719/225952789-444f10a5-443e-4009-83c1-dd963c258a6a.png)

Après choisissez "Génération des fichiers interceptés", ensuite sélectionnez un dossier où vous désirez placer les fichiers interceptés. En effet, les fichiers interceptés représentent les messages interceptés par les alliées pendant la Seconde Guerre mondiale. Ils sont nécessaires pour effectuer une attaque.

![image](https://user-images.githubusercontent.com/81489719/225953701-aded096f-dad5-45ed-93c9-e136187809c8.png)

Après avoir sélectionné votre dossier, la fenêtre au ci-dessus s'ouvre. Il faudra saisir le Grundstellung (le premier trigramme de la dernière colonne dans l'entête du fichier). Puis, cliquez sur "OK".

![Screenshot 2023-03-17 165430](https://user-images.githubusercontent.com/81489719/225955401-c77f94d0-b400-4c19-89fd-9cb5bf3dd86c.png)

Maintenant, vous pouvez effectuer une attaque sur le message. Vous allez cliquer sur "Attaque" en haut dans la barre de menu, puis cliquez sur "Attaque sur rotors et anneaux". En effet, ici il s'agit que de l'attaque sur les paramètres de l'anneau, ainsi que la position des rotors, nous allons devoir ensuite faire une attaque sur le tableau de connexion. 

Suite à cela, vous allez choisir le dossier des interceptions où vous avez placé les fichiers interceptionés. Ensuite, vous allez choisir le fichier qui contient le message. L'attaque prends ensuite quelques secondes. Vous allez avoir à la fin une fenêtre avec les solutions possibles, puisqu'il peut y'en avoir plusieurs. Vous devez les vérifier vous mêmes. 

![image](https://user-images.githubusercontent.com/81489719/225991661-36860d52-ee01-48bb-b6c0-465390930d49.png)

Après avoir réecris retrouvé le message avec la clé solution (on peut la trouver en chiffrant les deux trigrammes de l'entête du fichier chiffré) vous allez écrire ce message dans un fichier, ce message est en fait le message en clair sans la connaisance du tableau de connexion. Vous allez ensuite cliquer sur "Attaque" puis sur "Attaque sur le tableau de connexion". Vous allez ensuite choisir le fichier avec le message que vous venez de saisir. A la fin de l'attaque vous aurez une fenêtre avec les solutions de l'attaque sur le tableau de connexion.

![image](https://user-images.githubusercontent.com/81489719/225992345-76560d3f-1aea-49c5-8a63-9ffae4cd2698.png)

Attention l'attaque ne fonctionne pas à tous les coups, c'est d'ailleurs le défaut de l'attaque polonaise.
Une autre raison explique ce problème : toutes les fonctions nécessaire à l'attaque "polonaise" n'ont pas été implanté.
