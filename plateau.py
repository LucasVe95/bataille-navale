# -----------------------------
# Classes de base
# -----------------------------
class Coord:
    def __init__(self, coord_str):
        lettres = "ABCDEFGHIJ"
        if len(coord_str) < 2 or coord_str[0].upper() not in lettres or not coord_str[1:].isdigit():
            raise ValueError("Coordonnée invalide")
        self.row = lettres.index(coord_str[0].upper())
        self.col = int(coord_str[1:]) - 1
        if self.col < 0 or self.col > 9:
            raise ValueError("Coordonnée invalide")

class Bateau:
    def __init__(self, type):
        types_valides = ['torpilleur', 'contre torpilleur', 'sous-marin', 'croiseur', 'porte-avions']
        if type not in types_valides:
            raise ValueError("Type de bateau invalide")
        self.type = type
        self.cases = []
        self.taille = {'torpilleur': 2, 'contre torpilleur': 3, 'sous-marin': 3,
                       'croiseur': 4, 'porte-avions': 5}[type]

class Battaille_Navale:
    def __init__(self):
        self.grid_size = 10
        self.plateau = [["O" for _ in range(self.grid_size)] for _ in range(self.grid_size)]

    def __str__(self):
        print("  " + " ".join(str(i+1) for i in range(self.grid_size)))
        for i, row in enumerate(self.plateau):
            print(chr(ord('A') + i) + " " + " ".join(row))

    def tirer(self, coord: Coord):
        r, c = coord.row, coord.col
        val = self.plateau[r][c]
        if val in ["X", "O"]:
            return None
        if val == "B":
            self.plateau[r][c] = "X"
            return True
        else:
            self.plateau[r][c] = "O"
            return False

# -----------------------------
# Classe joueur
# -----------------------------
class Player:
    def __init__(self, name):
        self.name = name
        self.plateau = Battaille_Navale()
        self.types_restants = ['torpilleur', 'contre torpilleur', 'sous-marin', 'croiseur', 'porte-avions']
        self.bateaux_restants = []
        self.cases_attaquable = {f"{lettre}{num}": True for lettre in "ABCDEFGHIJ" for num in range(1, 11)}

    def placer_bateau(self, type, emplacement, orientation):
        bateau = Bateau(type)
        if type not in self.types_restants:
            raise ValueError("Type de bateau déjà placé")
        lettres = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,'I':8,'J':9}
        ligne = lettres[emplacement[0].upper()]
        colone = int(emplacement[1:]) - 1
        # Vérification et placement
        for i in range(bateau.taille):
            if orientation == 'N':
                r, c = ligne - i, colone
            elif orientation == 'S':
                r, c = ligne + i, colone
            elif orientation == 'E':
                r, c = ligne, colone + i
            elif orientation == 'W':
                r, c = ligne, colone - i
            else:
                raise ValueError("Orientation invalide")
            if not (0 <= r < 10 and 0 <= c < 10):
                raise ValueError("Placement hors de la grille")
            if self.plateau.plateau[r][c] == "X":
                raise ValueError("Collision avec un autre bateau")
        # Placement final
        for i in range(bateau.taille):
            if orientation == 'N':
                r, c = ligne - i, colone
            elif orientation == 'S':
                r, c = ligne + i, colone
            elif orientation == 'E':
                r, c = ligne, colone + i
            elif orientation == 'W':
                r, c = ligne, colone - i
            self.plateau.plateau[r][c] = "B"
            bateau.cases.append(chr(ord('A') + r) + str(c + 1))
        self.bateaux_restants.append(bateau)
        self.types_restants.remove(type)

    def est_valide(self, coord_str):
        return bool(self.cases_attaquable.get(coord_str, False))

# -----------------------------
# Fonction tour
# -----------------------------
def tour(joueur_actuel, coord_str):
    if not joueur_actuel.est_valide(coord_str):
        print(f"La case {coord_str} a déjà été ciblée ou est invalide.")
        return
    joueur_actuel.cases_attaquable[coord_str] = False
    try:
        coord = Coord(coord_str)
    except ValueError:
        print("Coordonnée invalide. Réessayez.")
        return
    resultat = joueur_actuel.plateau.tirer(coord)
    if resultat is None:
        print(f"La case {coord_str} a déjà été ciblée.")
    elif resultat:
        print(f"Tir sur {coord_str} : touché !")
    else:
        print(f"Tir sur {coord_str} : dans l'eau.")

# -----------------------------
# Fonction partie
# -----------------------------
def partie():
    j1 = Player(input("Nom du Joueur 1: "))
    j2 = Player(input("Nom du Joueur 2: "))
    # Placement des bateaux
    for joueur in [j1, j2]:
        while joueur.types_restants:
            print(f"{joueur.name}, votre plateau actuel :")
            joueur.plateau.__str__()
            bateau_type = input(f"Quel bateau placer parmi {joueur.types_restants} ? ").lower()
            coord = input("Coordonnée de départ (ex A1) : ")
            orientation = input("Orientation (N,S,E,W) : ").upper()
            try:
                joueur.placer_bateau(bateau_type, coord, orientation)
                print(f"{bateau_type} placé !")
            except ValueError as e:
                print("Erreur :", e)
    # Boucle de jeu
    joueur_actuel, joueur_adverse = j1, j2
    while True:
        print(f"{joueur_actuel.name}, à vous de tirer !")
        coord = input("Coordonnée à attaquer : ")
        tour(joueur_adverse, coord)
        # Changement de joueur
        joueur_actuel, joueur_adverse = joueur_adverse, joueur_actuel

# -----------------------------
# Lancer le jeu
# -----------------------------
if __name__ == "__main__":
    partie()
