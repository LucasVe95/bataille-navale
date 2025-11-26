class Battaille_Navale:
    def __init__(self):
        self.grid_size = 10
        self.plateau = [["°" for i in range(self.grid_size)] for i in range(self.grid_size)]
    def __str__(self):
        """Afficher une grille vide avec des cellules identifiables (A1, B2, etc.)."""
        # Afficher l'en-tête des colonnes
        print("  " + " ".join([str(i + 1) for i in range(self.grid_size)]))
        for row_numero in range(self.grid_size):
            # Afficher l'identifiant de la ligne (A, B, C, ...)
            row_nom = chr(ord('A') + row_numero)
            # Afficher la ligne avec son identifiant
            print(row_nom + " " + " ".join(self.plateau[row_numero]))

#TEST UNITAIRE
if __name__ == "__main__":
    plateau = Battaille_Navale()
    plateau.__str__()
