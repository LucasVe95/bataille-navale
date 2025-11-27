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
        self.bateaux_restants = ['Torpilleur', 'Contre torpilleur', 'Sous-marin', 'Croiseur', 'Porte-avions']
        self.bateaux = []

    
    def placer_bateau(self, type, emplacement, orientation):
        if type not in self.bateaux_restants:
            raise ValueError("Type de bateau invalide ou déjà placé")
        bateau = Bateau(type)
        colone = int(emplacement[1])
        lettres = {'A' : 0, 'B' : 1, 'C' : 2, 'D' : 3, 'E' : 4, 'F' : 5, 'G' : 6, 'H' : 7, 'I' : 8, 'J' : 9}
        ligne = lettres[emplacement[0]]
        if orientation == 'N':
            for i in range(bateau.taille):
                if colone < 1 or colone > 10 or ligne - i < 0 or ligne - i > 9:
                    raise ValueError("Placement hors de la grille")
                self.plateau.plateau[ligne - i][colone - 1] = "X"
        elif orientation == 'S':
            for i in range(bateau.taille):
                if colone < 1 or colone > 10 or ligne + i > 9 or ligne + i < 0:
                    raise ValueError("Placement hors de la grille")
                self.plateau.plateau[ligne + i][colone - 1] = "X"
        elif orientation == 'E':
            for i in range(bateau.taille):
                if ligne < 0 or ligne > 9 or colone + i > 10 or colone + i < 1:
                    raise ValueError("Placement hors de la grille")
                self.plateau.plateau[ligne][colone + i - 1] = "X"
        elif orientation == 'W':
            for i in range(bateau.taille):
                if ligne < 0 or ligne > 9 or colone - i < 1 or colone - i > 10:
                    raise ValueError("Placement hors de la grille")
                self.plateau.plateau[ligne][colone - i - 1] = "X"
            



class Bateau:
    def __init__(self, type):
        self.type = type
        self.cases = []
        if type == 'Torpilleur':
            self.taille = 2
        elif type == 'Contre torpilleur' or type == 'Sous-marin':
            self.taille = 3
        elif type == 'Croiseur':
            self.taille = 4
        elif type == 'Porte-avions':
            self.taille = 5



#TEST UNITAIRE
if __name__ == "__main__":
    j1 = Player("Joueur 1")
    j1.plateau.__str__()
    j2 = Player("Joueur 2")
    j2.plateau.__str__()
    # Test de placement de bateau
    try:
        j1.placer_bateau('Torpilleur', 'A1', 'S')
        j1.plateau.__str__()
    except ValueError as e:
        print(e)
    try:
        j2.placer_bateau('Porte-avions', 'J10', 'N')
        j2.plateau.__str__()
    except ValueError as e:
        print(e)
    try:
        j1.placer_bateau('torpilleur', 'E5', 'E')
        j1.plateau.__str__()
    except ValueError as e:
        print(e)
#TEST UNITAIRE