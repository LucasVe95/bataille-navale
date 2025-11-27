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
    """En tant que joueur, je veux pouvoir sélectionner une case pour attaquer la grille de l’adversaire( la grille est une matrice 10x10)
    afin de tenter de toucher un bateau avec la class Battaille_Navale. qui crée une grille vide et affiche les coordonnées des cellules. en temps reel. et ansi de suite.
    """
    def est_valide(self, coord):
        """
        Vérifie si les coordonnées données sont valides pour une grille.
        
        Args:
            coord (str): Les coordonnées à vérifier (ex: 'A1', 'B5', etc.).
            taille_grille (int): La taille de la grille (par défaut 10 pour une grille 10x10).
            
        Returns:
            bool: True si les coordonnées sont valides, False sinon.
        """
        if len(coord) < 2 or len(coord) > 3:
            return False
        
        ligne = coord[0].upper()
        colonne = coord[1:]
        
        if not ('A' <= ligne <= chr(ord('A') + self.grid_size - 1)):
            return False
        
        if not colonne.isdigit():
            return False
        
        colonne_num = int(colonne)
        if not (1 <= colonne_num <= self.grid_size):
            return False
        
        return True
    def tours(self, coord):
        """Permet de gerer les tours des joueurs en alternant entre eux après chaque attaque."""
        if self.est_valide(coord):
            print(f"Attaque sur la case {coord} est valide.")
        else:
            print(f"Attaque sur la case {coord} est invalide.")
        
#TEST UNITAIRE
if __name__ == "__main__":
    plateau = Battaille_Navale()
    print(plateau)
    test_coords = ['A1', 'B5', 'J10', 'K1', 'A0', 'A11', 'AA', '5B']
    for coord in test_coords:
        plateau.tours(coord)
    print(plateau)