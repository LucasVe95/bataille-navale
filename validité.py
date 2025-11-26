"""En tant que joueur, je veux pouvoir sélectionner une case pour attaquer la grille de l’adversaire( la grille est une matrice 10x10)
afin de tenter de toucher un bateau avec la class Battaille_Navale. qui crée une grille vide et affiche les coordonnées des cellules. en temps reel. et ansi de suite.
"""
def est_valide(coord, taille_grille=10):
    """
    Vérifie si les coordonnées données sont valides pour une grille de taille spécifiée.
    
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
    
    if not ('A' <= ligne <= chr(ord('A') + taille_grille - 1)):
        return False
    
    if not colonne.isdigit():
        return False
    
    colonne_num = int(colonne)
    if not (1 <= colonne_num <= taille_grille):
        return False
    
    return True
#TEST UNITAIRE
if __name__ == "__main__":   
    test_coords = ['A1', 'B5', 'J10', 'K1', 'A0', 'A11', 'AA', '5B']
    for coord in test_coords:
        print(f"Coordonnée {coord} est valide: {est_valide(coord)}")