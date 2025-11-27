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
        self.bateaux_restants = ['torpilleur', 'contre torpilleur', 'sous-marin', 'croiseur', 'porte-avions']
        self.bateaux = []

    
    def placer_bateau(self, type, emplacement, orientation):
        bateau = Bateau(type)
        if type not in self.bateaux_restants:
            raise ValueError("Type de bateau déjà placé")
        if len(emplacement) < 1 or emplacement[0] not in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'] or int(emplacement[1]) < 1 or int(emplacement[1]) > 10:
            raise ValueError("Case de départ invalide")
        if orientation not in ['N', 'S', 'E', 'W']:
            raise ValueError("Orientation invalide")
        colone = int(emplacement[1])
        lettres = {'A' : 0, 'B' : 1, 'C' : 2, 'D' : 3, 'E' : 4, 'F' : 5, 'G' : 6, 'H' : 7, 'I' : 8, 'J' : 9}
        ligne = lettres[emplacement[0]]
        if orientation == 'N':
            for i in range(bateau.taille):
                if colone < 1 or colone > 10 or ligne - i < 0 or ligne - i > 9:
                    raise ValueError("Placement hors de la grille")
                if self.plateau.plateau[ligne - i][colone - 1] == "X":
                    raise ValueError("Placement en collision avec un autre bateau")
            for i in range(bateau.taille):
                self.plateau.plateau[ligne - i][colone - 1] = "X"
                bateau.cases.append(emplacement[0] + str(colone - 0 + i))
        elif orientation == 'S':
            for i in range(bateau.taille):
                if colone < 1 or colone > 10 or ligne + i < 0 or ligne + i > 9:
                    raise ValueError("Placement hors de la grille")
                if self.plateau.plateau[ligne + i][colone - 1] == "X":
                    raise ValueError("Placement en collision avec un autre bateau")
            for i in range(bateau.taille):
                self.plateau.plateau[ligne + i][colone - 1] = "X"
                bateau.cases.append(emplacement[0] + str(colone + i))
        elif orientation == 'E':
            for i in range(bateau.taille):
                if colone - 1 + i < 0 or colone - 1 + i > 9 or ligne < 0 or ligne > 9:
                    raise ValueError("Placement hors de la grille")
                if self.plateau.plateau[ligne][colone - 1 + i] == "X":
                    raise ValueError("Placement en collision avec un autre bateau")
            for i in range(bateau.taille):
                self.plateau.plateau[ligne][colone - 1 + i] = "X"
                bateau.cases.append(emplacement[0] + str(colone + i))
        elif orientation == 'W':
            for i in range(bateau.taille):
                if colone - 1 - i < 0 or colone - 1 - i > 9 or ligne < 0 or ligne > 9:
                    raise ValueError("Placement hors de la grille")
                if self.plateau.plateau[ligne][colone - 1 - i] == "X":
                    raise ValueError("Placement en collision avec un autre bateau")
            for i in range(bateau.taille):
                self.plateau.plateau[ligne][colone - 1 - i] = "X"
                bateau.cases.append(emplacement[0] + str(colone - i))
        self.bateaux.append(bateau)
        self.bateaux_restants.remove(type)
            



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

def tour(joueur_actuel, adversaire):
    print(f"C'est le tour de {joueur_actuel.name}.")
    # attaquer

def partie():
    j1 = Player(input("Nom du Joueur 1: "))
    j2 = Player(input("Nom du Joueur 2: "))
    # placement de bateau
    while j1.bateaux_restants:
        bateau_type = input(f"{j1.name}, quel bateau voulez-vous placer parmi [{', '.join(j1.bateaux_restants)}] ? ").capitalize().lower()
        coordonnée = input("Entrez les coordonnés de la première case du bateau: ")
        orientation = input("Entrez l'orientation du bateau (N, S, E, W): ")
        try:
            j1.placer_bateau(bateau_type, coordonnée, orientation)
            j1.plateau.__str__()
            print(f"{bateau_type} placé avec succès.")
        except ValueError as e:
            j1.plateau.__str__()
            print(f"Erreur lors du placement de {bateau_type}: {e}")
    while j2.bateaux_restants:
        bateau_type = input(f"{j2.name}, quel bateau voulez-vous placer parmi [{', '.join(j2.bateaux_restants)}] ? ").capitalize().lower()
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
        tour(j1, j2)
        tour(j2, j1)
#TEST UNITAIRE
if __name__ == "__main__":
    partie()
#TEST UNITAIRE