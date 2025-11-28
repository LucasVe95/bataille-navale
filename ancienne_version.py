class Coord:
    def __init__(self, coord_str):
        lettres = "ABCDEFGHIJ"
        self.coord_str = coord_str
        if len(coord_str) < 2 or coord_str[0].upper() not in lettres or not coord_str[1:].isdigit():
            raise ValueError("Coordonnée invalide")
        self.row = lettres.index(coord_str[0].upper())
        self.col = int(coord_str[1:]) - 1
        if self.col < 0 or self.col > 9:
            raise ValueError("Coordonnée invalide")
        
class Battaille_Navale:
    def __init__(self):
        self.grid_size = 10
        self.plateau = [["." for i in range(self.grid_size)] for i in range(self.grid_size)]
        self.bateaux = []

    def __str__(self):
        """Afficher une grille vide avec des cellules identifiables (A1, B2, etc.)."""
        # Afficher l'en-tête des colonnes
        print("  " + " ".join([str(i + 1) for i in range(self.grid_size)]))
        for row_numero in range(self.grid_size):
            # Afficher l'identifiant de la ligne (A, B, C, ...)
            row_nom = chr(ord('A') + row_numero)
            # Afficher la ligne avec son identifiant
            print(row_nom + " " + " ".join(self.plateau[row_numero]))
    

class Player:
    def __init__(self, name):
        self.name = name
        self.plateau = Battaille_Navale()
        self.plateau_vis = Battaille_Navale()
        self.types_restants = ['torpilleur', 'contre torpilleur', 'sous-marin', 'croiseur', 'porte-avions']
        self.cases_attaquable = {f"{lettre}{num}": True for lettre in "ABCDEFGHIJ" for num in range(1, 11)}

    def placer_bateau(self, type, emplacement, orientation):
        bateau = Bateau(type)
        n = len(emplacement)
        # Vérifications des variables entrées

        # Type de bateau valide
        if type not in self.types_restants:
            raise ValueError("Type de bateau déjà placé")
        
        # orthographe de la case de départ valide
        if n < 2 or n > 3:
            raise ValueError("La case de départ doit être composée de la lettre de la ligne et du numéro de la colonne")
        
        # lettre de la ligne allant de A à J
        if emplacement[0] not in 'ABCDEFGHIJ':
            raise ValueError("Lettre de la ligne invalide")
        
        # numéro de la colonne entre 1 et 10
        if int(emplacement[1]) < 1:
            raise ValueError("le numéro de la colonne doit être entre 1 et 10")
        if n == 3:
            if int(emplacement[2]) > 0 or int(emplacement[1]) != 1:
                raise ValueError("le numéro de la colonne doit être entre 1 et 10")
            
        # orientation valide
        if orientation not in 'NSEW':
            raise ValueError("Orientation invalide \nrappel: les orientations disponibles sont N, S, E et W")
        
        # Conversion des coordonnées
        colone = int(emplacement[1:]) - 1
        lettres = {'A' : 0, 'B' : 1, 'C' : 2, 'D' : 3, 'E' : 4, 'F' : 5, 'G' : 6, 'H' : 7, 'I' : 8, 'J' : 9}
        ligne = lettres[emplacement[0]]
        # Vérifications de placement
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
            bateau.cases.append(f"{chr(ord('A') + r)}{c + 1}")
        self.plateau.bateaux.append(bateau)
        self.types_restants.remove(type)
        # Ajout du bateau à la liste des bateaux du joueur et suppression de ce type de bateau des bateaux restants
    
    def est_valide(self, coord):
        """
        Vérifie si les coordonnées données sont valides pour l'attaque.

        Returns:
            bool: True si les coordonnées sont valides, False sinon.
        """
        return self.cases_attaquable.get(coord, False)
    
    def tirer(self, coord: Coord):
        r, c = coord.row, coord.col
        val = self.plateau.plateau[r][c]
        coord_str = coord.coord_str
        if val in ["X", "O"]:
            return None
        if val == "B":
            self.plateau_vis.plateau[r][c] = "X"
            self.plateau.plateau[r][c] = "X"
            for bateau in self.plateau.bateaux:
                if coord_str in bateau.cases:
                    bateau.cases.remove(coord_str)
                    if not bateau.cases:
                        print(f"tir sur {coord_str} : Bateau {bateau.type} coulé !")
                        self.plateau.bateaux.remove(bateau)
                        return 'coule'
            return True
        else:
            self.plateau_vis.plateau[r][c] = "O"
            self.plateau.plateau[r][c] = "O"
            return False


class Bateau:
    def __init__(self, type):
        if type not in ['torpilleur', 'contre torpilleur', 'sous-marin', 'croiseur', 'porte-avions']:
            raise ValueError("Type de bateau invalide")
        self.type = type
        self.cases = []
        if type == 'torpilleur':
            self.taille = 2
        elif type == 'contre torpilleur' or type == 'sous-marin':
            self.taille = 3
        elif type == 'croiseur':
            self.taille = 4
        elif type == 'porte-avions':
            self.taille = 5

def tour(joueur_actuel, coord_str):
    if not joueur_actuel.est_valide(coord_str):
        print(f"La case {coord_str} a déjà été ciblée ou est invalide.")
        return False
    joueur_actuel.cases_attaquable[coord_str] = False
    try:
        coord = Coord(coord_str)
    except ValueError:
        print("Coordonnée invalide. Réessayez.")
        return False
    resultat = joueur_actuel.tirer(coord)
    if resultat is None:
        print(f"La case {coord_str} a déjà été ciblée.")
    elif resultat == True and resultat != 'coule':
        print(f"Tir sur {coord_str} : touché !")
    elif resultat == 'coule':
        pass
    else:
        print(f"Tir sur {coord_str} : dans l'eau.")
    return True

    

def partie():
    j1 = Player(input("Nom du Joueur 1: "))
    j2 = Player(input("Nom du Joueur 2: "))
    # Placement des bateaux
    for joueur in [j1, j2]:
        while joueur.types_restants:
            print(f"{joueur.name}, votre plateau actuel :")
            joueur.plateau.__str__()
            bateau_type = input(f"Quel bateau placer parmi {joueur.types_restants} ? ").lower()
            coord = input("Coordonnée de départ : ").upper()
            orientation = input("Orientation (N,S,E,W) : ").upper()
            try:
                joueur.placer_bateau(bateau_type, coord, orientation)
                print(f"{bateau_type} placé !")
            except ValueError as e:
                print("Erreur :", e)
    # Boucle de jeu
    joueur_actuel, joueur_adverse = j1, j2
    while joueur_actuel.plateau.bateaux and joueur_adverse.plateau.bateaux:
        joueur_adverse.plateau_vis.__str__()
        print(f"{joueur_actuel.name}, à vous de tirer !")
        coord = input("Coordonnée à attaquer : ").upper()
        result = tour(joueur_adverse, coord)
        # Changement de joueur
        if result == True and joueur_adverse.plateau.bateaux:
            joueur_actuel, joueur_adverse = joueur_adverse, joueur_actuel
    print(f"Plateau final de {joueur_actuel.name} :")
    joueur_actuel.plateau.__str__()
    print(f"Plateau final de {joueur_adverse.name} :")
    joueur_adverse.plateau.__str__()
    print(f"Félicitations commandant {joueur_actuel.name}, la victoire est vôtre !")
        

#TEST UNITAIRE
if __name__ == "__main__":
    partie()
