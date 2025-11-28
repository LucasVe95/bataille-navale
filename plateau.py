import tkinter as tk
import random
from tkinter import simpledialog

# ------------------------
# Constantes / Types
# ------------------------
TAILLE = 10
BATEAUX_DEFS = {
    'torpilleur': 2,
    'contre torpilleur': 3,
    'sous-marin': 3,
    'croiseur': 4,
    'porte-avions': 5
}
LETTRES = "ABCDEFGHIJ"

# ------------------------
# Class par ICI
# ------------------------
class Coord:
    def __init__(self, coord_str):
        coord_str = coord_str.strip().upper()
        self.coord_str = coord_str
        if len(coord_str) < 2 or coord_str[0] not in LETTRES or not coord_str[1:].isdigit():
            raise ValueError("Coordonnée invalide")
        self.row = LETTRES.index(coord_str[0])
        self.col = int(coord_str[1:]) - 1
        if self.col < 0 or self.col >= TAILLE:
            raise ValueError("Coordonnée invalide")

    def __repr__(self):
        return f"{self.coord_str}"

class Ship:
    def __init__(self, type_name):
        if type_name not in BATEAUX_DEFS:
            raise ValueError("Type de bateau invalide")
        self.type = type_name
        self.size = BATEAUX_DEFS[type_name]
        self.positions = []  # list of "A1" style strings

    def is_sunk(self):
        return len(self.positions) == 0

class GameBoard:
    """
    Représente le plateau interne (positions des bateaux + état des tirs).
    plateau[r][c] : "." empty, "B" bateau présent, "X" touché, "O" raté
    """
    def __init__(self, size=TAILLE):
        self.size = size
        self.plateau = [["." for _ in range(size)] for _ in range(size)]
        self.ships = []

    def place_ship(self, ship: Ship, start_row, start_col, orientation):
        # vérifie si possible, pose et enregistre les positions (A1 style)
        positions = []
        for i in range(ship.size):
            if orientation == 'N':
                r, c = start_row - i, start_col
            elif orientation == 'S':
                r, c = start_row + i, start_col
            elif orientation == 'E':
                r, c = start_row, start_col + i
            elif orientation == 'W':
                r, c = start_row, start_col - i
            else:
                raise ValueError("Orientation invalide")

            if not (0 <= r < self.size and 0 <= c < self.size):
                raise ValueError("Placement hors plateau")
            if self.plateau[r][c] == "B":
                raise ValueError("Collision avec un autre bateau")
            positions.append((r, c))

        
        # Position finale
        for r, c in positions:
            self.plateau[r][c] = "B"
            ship.positions.append(f"{LETTRES[r]}{c+1}")
        self.ships.append(ship)

    def receive_shot(self, row, col):
        """
        Reçoit un tir sur (row,col).
        Retourne: 'hit', 'miss', 'sunk' et le type du bateau si coulé, ou None si case déjà tirée.
        """
        val = self.plateau[row][col]
        coord_str = f"{LETTRES[row]}{col+1}"
        if val in ("X", "O"):
            return None  # case déjà ciblée

        if val == "B":
            # touché
            self.plateau[row][col] = "X"
            # chercher le bateau et retirer la case
            for ship in self.ships:
                if coord_str in ship.positions:
                    ship.positions.remove(coord_str)
                    if ship.is_sunk():
                        # supprimer le navire de la liste
                        self.ships.remove(ship)
                        return ('sunk', ship.type)
                    else:
                        return ('hit', None)
            # improbable mais au cas où
            return ('hit', None)
        else:
            self.plateau[row][col] = "O"
            return ('miss', None)

    def all_sunk(self):
        return len(self.ships) == 0

# ------------------------
# Classe Joueur ()
# ------------------------
class PlayerLogic:
    def __init__(self, name, is_ia=False):
        self.name = name
        self.is_ia = is_ia
        self.board = GameBoard()
        self.view = GameBoard()  # ce que l'on voit de l'adversaire (X/O)
        self.types_restants = list(BATEAUX_DEFS.keys())
        # cases attaquables map "A1": True/False
        self.cases_attaquable = {f"{lett}{num}": True for lett in LETTRES for num in range(1, TAILLE+1)}
        # pour IA avancée - file cible quand on a touché
        self.ia_target_queue = []  # list of (r,c) à tester en priorité

    def place_ship_random(self, type_name):
        ship = Ship(type_name)
        placed = False
        attempts = 0
        while not placed and attempts < 200:
            attempts += 1
            ori = random.choice(['N','S','E','W'])
            r = random.randint(0, TAILLE-1)
            c = random.randint(0, TAILLE-1)
            try:
                self.board.place_ship(ship, r, c, ori)
                placed = True
            except Exception:
                continue
        if not placed:
            raise RuntimeError("Impossible de placer le bateau aléatoirement")
        if type_name in self.types_restants:
            self.types_restants.remove(type_name)

    def can_attack(self, coord_str):
        return self.cases_attaquable.get(coord_str, False)

    def mark_attacked(self, coord_str):
        if coord_str in self.cases_attaquable:
            self.cases_attaquable[coord_str] = False

    def choose_ia_shot(self):
        # IA basique avec mode "target" : si queue non vide, pop it; sinon random available
        if self.ia_target_queue:
            return self.ia_target_queue.pop(0)
        options = [ (r,c) for r in range(TAILLE) for c in range(TAILLE)
                    if self.view.plateau[r][c] == "." and f"{LETTRES[r]}{c+1}" in self.cases_attaquable and self.cases_attaquable[f"{LETTRES[r]}{c+1}"] ]
        if not options:
            return None
        return random.choice(options)

    def enqueue_adjacent(self, r, c):
        # Ajoute voisins valides dans la queue (N,S,E,W) pour viser quand on touche
        candidates = [(r-1,c),(r+1,c),(r,c-1),(r,c+1)]
        for rr, cc in candidates:
            if 0 <= rr < TAILLE and 0 <= cc < TAILLE:
                coord_str = f"{LETTRES[rr]}{cc+1}"
                if self.cases_attaquable.get(coord_str, False):
                    # éviter doublons
                    if (rr,cc) not in self.ia_target_queue:
                        self.ia_target_queue.append((rr,cc))

# ------------------------
# GUI (Nouvelle version) 
# ------------------------
class BatailleNavaleGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Bataille Navale")
        self.mode = tk.StringVar(value="IA")
        self.joueurs = []
        self.joueur_actuel_idx = 0  # index dans self.joueurs
        self.bateau_a_placer = None
        self.orientation = 'E'
        self.header_frame = None
        self.grid_frame = None
        self.buttons = []        # boutons actuels (grille affichée)
        self.info_tir = None     # label Touché/Dans l'eau
        self.init_menu()

    # ---------- menu ----------
    def init_menu(self):
        self.clear_all()
        tk.Label(self.root, text="Choisir le mode de jeu:").pack(pady=6)
        tk.Radiobutton(self.root, text="PvIA", variable=self.mode, value="IA").pack()
        tk.Radiobutton(self.root, text="PvP", variable=self.mode, value="PVP").pack()
        tk.Button(self.root, text="Valider", command=self.start_game).pack(pady=6)

    def start_game(self):
        mode = self.mode.get()
        self.clear_all()
        if mode == "IA":
            nom = simpledialog.askstring("Nom", "Nom du joueur :") or "Joueur"
            self.joueurs = [PlayerLogic(nom), PlayerLogic("IA", is_ia=True)]
        else:
            nom1 = simpledialog.askstring("Nom", "Nom Joueur 1 :") or "J1"
            nom2 = simpledialog.askstring("Nom", "Nom Joueur 2 :") or "J2"
            self.joueurs = [PlayerLogic(nom1), PlayerLogic(nom2)]
        self.joueur_actuel_idx = 0
        # commencer la phase de placement pour joueur 0
        self.phase_placement()

    # ---------- placement ----------
    def phase_placement(self):
        # Affiche la phase de placement pour self.joueur_actuel_idx
        self.clear_all()
        joueur = self.joueurs[self.joueur_actuel_idx]

        if joueur.types_restants:
            self.bateau_a_placer = joueur.types_restants[0]
            # header
            self.header_frame = tk.Frame(self.root)
            self.header_frame.pack(pady=6)
            tk.Label(self.header_frame, text=f"{joueur.name}, placez votre {self.bateau_a_placer} (taille {BATEAUX_DEFS[self.bateau_a_placer]})").pack()
            frame_o = tk.Frame(self.header_frame)
            frame_o.pack(pady=4)
            for ori in ['N', 'E', 'S', 'W']:
                tk.Button(frame_o, text=ori, width=3, command=lambda o=ori: self.set_orientation(o)).pack(side="left", padx=2)
            tk.Label(self.header_frame, text="Cliquez sur la case de départ.").pack(pady=4)
            # grille du joueur (afficher B pendant placement)
            self.create_plateau(joueur, placer=True)
        else:
            # ce joueur a fini ; on passe au suivant ou on commence la phase de tir
            if self.joueur_actuel_idx == 0:
                self.joueur_actuel_idx = 1
                if self.joueurs[self.joueur_actuel_idx].is_ia:
                    # IA place tout aléatoirement
                    ia = self.joueurs[self.joueur_actuel_idx]
                    for t in list(ia.types_restants):
                        ia.place_ship_random(t)
                    ia.types_restants.clear()
                    # revenir au joueur 0 et commencer tir
                    self.joueur_actuel_idx = 0
                    self.phase_tir()
                else:
                    self.phase_placement()
            else:
                # si on était joueur 1, revenir à 0 et commencer tir
                self.joueur_actuel_idx = 0
                self.phase_tir()

    def set_orientation(self, ori):
        self.orientation = ori

    def placer_bateau_click(self, row, col):
        joueur = self.joueurs[self.joueur_actuel_idx]
        type_bat = self.bateau_a_placer
        ship = Ship(type_bat)
        try:
            joueur.board.place_ship(ship, row, col, self.orientation)
        except Exception as e:
            # pour debug on pourrait afficher message
            print("Placement invalide :", e)
            return
        # retirer le type posé si présent
        if type_bat in joueur.types_restants:
            joueur.types_restants.remove(type_bat)
        # réafficher la phase placement (soit prochain bateau, soit joueur suivant)
        self.phase_placement()

    # ---------- affichage plateau ----------
    def create_plateau(self, joueur_logic: PlayerLogic, placer=False):
        # détruit ancienne grid si existante
        if self.grid_frame:
            self.grid_frame.destroy()
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack(padx=6, pady=6)
        self.buttons = []

        # en placement, on montre le plateau du joueur (B visibles)
        # en tir, on montre la vue du joueur actif de l'adversaire (X/O) : on affiche adv.view
        board_to_show = joueur_logic.board if placer else joueur_logic.view

        for r in range(TAILLE):
            row_btns = []
            for c in range(TAILLE):
                val = board_to_show.plateau[r][c]
                if placer:
                    if val == "B":
                        text, couleur = "B", "green"
                    elif val == "X":
                        text, couleur = "X", "red"
                    elif val == "O":
                        text, couleur = "O", "lightblue"
                    else:
                        text, couleur = ".", "lightgray"
                else:
                    # phase tir : on voit X/O/.
                    if val == "X":
                        text, couleur = "X", "red"
                    elif val == "O":
                        text, couleur = "O", "lightblue"
                    else:
                        text, couleur = ".", "lightgray"

                b = tk.Button(self.grid_frame, text=text, width=3, height=1, bg=couleur)
                b.grid(row=r, column=c, padx=1, pady=1)

                if placer:
                    b.config(command=lambda r=r, c=c: self.placer_bateau_click(r, c))
                else:
                    b.config(command=lambda r=r, c=c: self.tirer_click(r, c))

                row_btns.append(b)
            self.buttons.append(row_btns)

    # ---------- phase tir ----------
    def phase_tir(self):
        # Affiche la vue du joueur actif (il voit la grille de l'adversaire)
        self.clear_header_and_grid()
        joueur = self.joueurs[self.joueur_actuel_idx]
        adv = self.joueurs[1 - self.joueur_actuel_idx]

        # header + info label
        self.header_frame = tk.Frame(self.root)
        self.header_frame.pack(pady=6)
        tk.Label(self.header_frame, text=f"{joueur.name}, à vous de tirer !").pack()
        self.info_tir = tk.Label(self.header_frame, text="", font=("Arial", 14))
        self.info_tir.pack()

        # afficher la grille de l'adversaire (bateaux invisibles - on montre joueur.view de l'adversaire)
        # la vue du joueur courant sur l'adversaire est joueur.view
        self.create_plateau(joueur, placer=False)

        # si l'IA doit jouer, on déclenche après un court délai
        if joueur.is_ia:
            self.root.after(500, self.ia_tirer)

    def tirer_click(self, row, col):
        joueur = self.joueurs[self.joueur_actuel_idx]
        adv = self.joueurs[1 - self.joueur_actuel_idx]
        coord_str = f"{LETTRES[row]}{col+1}"

        # si déjà ciblée -> ignore
        if not joueur.can_attack(coord_str):
            return

        # marquer ciblée côté attaquant
        joueur.mark_attacked(coord_str)

        # appliquer tir sur plateau adverse
        resultat = adv.board.receive_shot(row, col)
        # mettre à jour la vue de l'attaquant
        if resultat is None:
            # déjà ciblée (peu probable car can_attack prévient) => ignore
            return

        res_type, ship_type = resultat  # res_type in 'hit','miss','sunk'
        if res_type == 'hit':
            joueur.view.plateau[row][col] = "X"
            # si attaquant est IA et touche, il doit viser voisins
            if joueur.is_ia:
                joueur.enqueue_adjacent(row, col)
            # message
            if self.info_tir:
                self.info_tir.config(text="🎯 Touché !", fg="red")
            # vérifier victoire
            if adv.board.all_sunk():
                self.clear_header_and_grid()
                self.header_frame = tk.Frame(self.root)
                self.header_frame.pack(pady=10)
                tk.Label(self.header_frame, text=f"{joueur.name} a gagné !", font=("Arial", 16)).pack()
                return
            # le joueur rejoue (on réaffiche la grille de l'adversaire pour montrer X)
            self.create_plateau(joueur, placer=False)
        elif res_type == 'sunk':
            joueur.view.plateau[row][col] = "X"
            # si IA, on peut nettoyer queue (optionnel)
            if joueur.is_ia:
                # on pourrait enlever des cibles inconsistantes; on garde simple
                pass
            if self.info_tir:
                self.info_tir.config(text=f"💥 Coulé ({ship_type}) !", fg="darkred")
            # vérifier victoire
            if adv.board.all_sunk():
                self.clear_header_and_grid()
                self.header_frame = tk.Frame(self.root)
                self.header_frame.pack(pady=10)
                tk.Label(self.header_frame, text=f"{joueur.name} a gagné !", font=("Arial", 16)).pack()
                return
            # attaquant rejoue (dans les règles, coulé = rejoue)
            self.create_plateau(joueur, placer=False)
        else:  # 'miss'
            joueur.view.plateau[row][col] = "O"
            if self.info_tir:
                self.info_tir.config(text="💧 Dans l'eau !", fg="blue")
            # passe au joueur suivant
            self.joueur_actuel_idx = 1 - self.joueur_actuel_idx
            self.root.update()
            self.root.after(300, self.phase_tir)

    # ---------- IA ----------
    def ia_tirer(self):
        if not self.joueurs[self.joueur_actuel_idx].is_ia:
            return
        ia = self.joueurs[self.joueur_actuel_idx]
        adv = self.joueurs[1 - self.joueur_actuel_idx]
        choice = ia.choose_ia_shot()
        if choice is None:
            # plus d'options
            return
        row, col = choice
        # vérifier si case attaquable selon la map des cases
        coord_str = f"{LETTRES[row]}{col+1}"
        if not ia.can_attack(coord_str):
            # si non attaquable, on rappelle ia_tirer rapidement
            self.root.after(50, self.ia_tirer)
            return
        # effectuer tir
        self.tirer_click(row, col)

    # ---------- util ----------
    def clear_header_and_grid(self):
        # détruit header + grid frames mais garde autres widgets si besoin
        if self.header_frame:
            self.header_frame.destroy()
            self.header_frame = None
        if self.grid_frame:
            self.grid_frame.destroy()
            self.grid_frame = None
        self.buttons = []
        self.info_tir = None

    def clear_all(self):
        # détruit tout dans la fenêtre (menu complet)
        for w in self.root.winfo_children():
            w.destroy()
        self.header_frame = None
        self.grid_frame = None
        self.buttons = []
        self.info_tir = None

    def run(self):
        self.root.mainloop()

# ---------- lancer ----------
if __name__ == "__main__":
    app = BatailleNavaleGUI()
    app.run()
