class Validité:
    """
    sous clase de la class bataille navale pour valider afin de pouvoir sélectionner une case pour attaquer la grille de l’adversaire
    afin de tenter de toucher un bateau. Le programme vérifie la validité du placement avant chaque ajout.
    """
    def __init__(self):
        self.grid_size = 10
        self.valid_cells = [chr(ord('A') + i) + str(j + 1) for i in range(self.grid_size) for j in range(self.grid_size)]
    def est_valide(self, cell):
        """Vérifie si une cellule donnée est valide (ex: A1, B5, J10)."""
        return cell in self.valid_cells
#TEST UNITAIRE
if __name__ == "__main__":
    validité = Validité()
    # Test des cellules valides
    test_cells = ["A1", "B5", "J10", "K1", "A11", "Z3"]
    for cell in test_cells:
        print(f"La cellule {cell} est valide: {validité.est_valide(cell)}")