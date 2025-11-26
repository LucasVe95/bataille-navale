class Battaille_Navale:
    """
    Crée une grille vide et affiche les coordonnées des cellules en temps réel.en collone et en ligne.
    """
    def __init__(self):
        self.grid_size = 10
        self.plateau = [['O' for j in range(self.grid_size)] for i in range(self.grid_size)]
    def __str__(self):
        """
        Afficher une grille vide avec des cellules identifiables (A1, B2, etc.). pour chaque joueur en affichant la grille du joueur actuel, puis l'autre quand c'est son tour
        L'etat de la grille doit être mis à jour après chaque attaque pour refléter les touches et les ratés. puis remis a zero a la fin de la partie.En ligne et en collone.
        """
        affichage = "  " + " ".join([str(i + 1).rjust(2) for i in range(self.grid_size)]) + "\n"
        for i in range(self.grid_size):
            ligne = chr(ord('A') + i) + " " + " ".join(self.plateau[i][j].rjust(2) for j in range(self.grid_size))
            affichage += ligne + "\n"
        return affichage
#TEST UNITAIRE
if __name__ == "__main__":
    plateau = Battaille_Navale()
    print(plateau)