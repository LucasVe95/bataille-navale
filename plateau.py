class Battaille_Navale:
    def __init__(self):
        self.grid_size = 10
        self.plateau = [["O" for i in range(self.grid_size)] for i in range(self.grid_size)]

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
        self.types_restants = ['torpilleur', 'contre torpilleur', 'sous-marin', 'croiseur', 'porte-avions']
        self.bateaux_restants = []
        self.cases_attaquable = {}
        for lettre in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']:
            for num in range (1, 11):
                cases = f"{lettre}{num}"
                self.cases_attaquable[cases] = True

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
        if emplacement[0] not in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']:
            raise ValueError("Lettre de la ligne invalide")
        
        # numéro de la colonne entre 1 et 10
        if int(emplacement[1]) < 1:
            raise ValueError("le numéro de la colonne doit être entre 1 et 10")
        if n == 3:
            if int(emplacement[2]) > 0 or int(emplacement[1]) != 1:
                raise ValueError("le numéro de la colonne doit être entre 1 et 10")
            
        # orientation valide
        if orientation not in ['N', 'S', 'E', 'W']:
            raise ValueError("Orientation invalide \nrappel: les orientations disponibles sont N, S, E et W")
        
        # Conversion des coordonnées
        if n == 2:
            colone = int(emplacement[1])
        else:
            colone = int(f"{emplacement[1]}{emplacement[2]}")
        lettres = {'A' : 0, 'B' : 1, 'C' : 2, 'D' : 3, 'E' : 4, 'F' : 5, 'G' : 6, 'H' : 7, 'I' : 8, 'J' : 9}
        ligne = lettres[emplacement[0]]
        # Placement du bateau selon l'orientation
        #Nord
        if orientation == 'N':
            #verification placement du bateau
            for i in range(bateau.taille):
                if colone < 1 or colone > 10 or ligne - i < 0 or ligne - i > 9:
                    raise ValueError("Placement hors de la grille")
                if self.plateau.plateau[ligne - i][colone - 1] == "X":
                    raise ValueError("Placement en collision avec un autre bateau")
            #placement du bateau
            for i in range(bateau.taille):
                self.plateau.plateau[ligne - i][colone - 1] = "X"
                bateau.cases.append(emplacement[0] + str(colone - 0 + i))
        #Sud
        elif orientation == 'S':
            #verification placement du bateau
            for i in range(bateau.taille):
                if colone < 1 or colone > 10 or ligne + i < 0 or ligne + i > 9:
                    raise ValueError("Placement hors de la grille")
                if self.plateau.plateau[ligne + i][colone - 1] == "X":
                    print(self.plateau.plateau[ligne + i][colone - 1])
                    raise ValueError("Placement en collision avec un autre bateau")
            #placement du bateau
            for i in range(bateau.taille):
                self.plateau.plateau[ligne + i][colone - 1] = "X"
                bateau.cases.append(emplacement[0] + str(colone + i))
        #Est
        elif orientation == 'E':
            #verification placement du bateau
            for i in range(bateau.taille):
                if colone - 1 + i < 0 or colone - 1 + i > 9 or ligne < 0 or ligne > 9:
                    raise ValueError("Placement hors de la grille")
                if self.plateau.plateau[ligne][colone - 1 + i] == "X":
                    raise ValueError("Placement en collision avec un autre bateau")
            #placement du bateau
            for i in range(bateau.taille):
                self.plateau.plateau[ligne][colone - 1 + i] = "X"
                bateau.cases.append(emplacement[0] + str(colone + i))
        #Ouest
        elif orientation == 'W':
            #verification placement du bateau
            for i in range(bateau.taille):
                if colone - 1 - i < 0 or colone - 1 - i > 9 or ligne < 0 or ligne > 9:
                    raise ValueError("Placement hors de la grille")
                if self.plateau.plateau[ligne][colone - 1 - i] == "X":
                    raise ValueError("Placement en collision avec un autre bateau")
            #placement du bateau
            for i in range(bateau.taille):
                self.plateau.plateau[ligne][colone - 1 - i] = "X"
                bateau.cases.append(emplacement[0] + str(colone - i))
        # Ajout du bateau à la liste des bateaux du joueur et suppression de ce type de bateau des bateaux restants
        self.bateaux_restants.append(bateau)
        self.types_restants.remove(type)
    
    def est_valide(self, coord):
        """
        Vérifie si les coordonnées données sont valides pour l'attaque
        
        Args:
            coord (str): Les coordonnées à vérifier (ex: 'A1', 'B5', etc.).
            taille_grille (int): La taille de la grille (par défaut 10 pour une grille 10x10).
            
        Returns:
            bool: True si les coordonnées sont valides, False sinon.
        """
        return self.cases_attaquable.get(coord, False)


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

def tour(joueur_actuel, coord_attaque):
    if joueur_actuel.est_valide(coord_attaque):
        print(f"Attaque sur la case {coord_attaque} est valide.")
        # attaquer
    else:
        print(f"Attaque sur la case {coord_attaque} est invalide.")
    

def partie():
    j1 = Player(input("Nom du Joueur 1: "))
    j2 = Player(input("Nom du Joueur 2: "))
    joueur = j1
    # placement de bateau
    while j1.types_restants:
        bateau_type = input(f"{j1.name}, quel bateau voulez-vous placer parmi [{', '.join(j1.types_restants)}] ?").lower()
        coordonnée = input("Entrez les coordonnés de la première case du bateau: ").upper()
        orientation = input("Entrez l'orientation du bateau (N, S, E, W): ").upper()
        try:
            j1.placer_bateau(bateau_type, coordonnée, orientation)
            j1.plateau.__str__()
            print(f"{bateau_type} placé avec succès.")
        except ValueError as e:
            j1.plateau.__str__()
            print(f"Erreur lors du placement de {bateau_type}: {e}")
    while j2.types_restants:
        bateau_type = input(f"{j2.name}, quel bateau voulez-vous placer parmi [{', '.join(j2.types_restants)}] ?").lower()
        coordonnée = input("Entrez les coordonnés de la première case du bateau: ")
        orientation = input("Entrez l'orientation du bateau (N, S, E, W): ")
        try:
            j2.placer_bateau(bateau_type, coordonnée, orientation)
            j2.plateau.__str__()
            print(f"{bateau_type} placé avec succès.")
        except ValueError as e:
            j2.plateau.__str__()
            print(f"Erreur lors du placement de {bateau_type}: {e}")
    while True: # boucle principale de la partie, condition de fin à ajouter
        if joueur == j1:
            joueur = j2
        else:
            joueur = j1
        coord = input(f"{joueur.name}, entrez les coordonnées de la case à attaquer: ")
        tour(joueur, coord)
#TEST UNITAIRE
if __name__ == "__main__":
    partie()
#TEST UNITAIRE