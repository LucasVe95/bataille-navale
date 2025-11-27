import tkinter as tk
import random
from tkinter import simpledialog

TAILLE = 10
BATEAUX = {
    'torpilleur': 2,
    'contre torpilleur': 3,
    'sous-marin': 3,
    'croiseur': 4,
    'porte-avions': 5
}

# ------------------------
# Classe Bateau
# ------------------------
class Bateau:
    def __init__(self, type):
        self.type = type
        self.taille = BATEAUX[type]
        self.cases = []

# ------------------------
# Classe Player
# ------------------------
class Player:
    def __init__(self, name, is_ia=False):
        self.name = name
        self.is_ia = is_ia
        self.plateau = [["O"] * TAILLE for _ in range(TAILLE)]
        self.bateaux_restants = []
        self.types_restants = list(BATEAUX.keys())
        # True = case encore attaquable (n'a pas été tirée)
        self.cases_attaquable = [[True] * TAILLE for _ in range(TAILLE)]

    def placer_bateau_aleatoire(self, type):
        bateau = Bateau(type)
        placed = False
        while not placed:
            orientation = random.choice(['N', 'S', 'E', 'W'])
            row = random.randint(0, TAILLE - 1)
            col = random.randint(0, TAILLE - 1)
            try:
                self._placer_bateau_logique(bateau, row, col, orientation)
                placed = True
            except:
                continue

    def _placer_bateau_logique(self, bateau, row, col, orientation):
        positions = []
        for i in range(bateau.taille):
            if orientation == 'N':
                r, c = row - i, col
            elif orientation == 'S':
                r, c = row + i, col
            elif orientation == 'E':
                r, c = row, col + i
            elif orientation == 'W':
                r, c = row, col - i
            else:
                raise ValueError("Orientation invalide")

            if not (0 <= r < TAILLE and 0 <= c < TAILLE):
                raise ValueError("Hors plateau")
            if self.plateau[r][c] == "B":
                raise ValueError("Collision")

            positions.append((r, c))

        for r, c in positions:
            self.plateau[r][c] = "B"
            bateau.cases.append((r, c))

        self.bateaux_restants.append(bateau)

    def tous_coules(self):
        # renvoie True s'il n'y a plus de "B" dans le plateau
        return all(cell != "B" for row in self.plateau for cell in row)

# ------------------------
# GUI
# ------------------------
class BatailleNavaleGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Bataille Navale")

        self.mode = tk.StringVar(value="IA")
        self.joueurs = []
        self.joueur_actuel = 0
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
            self.joueurs = [Player(nom), Player("IA", is_ia=True)]
        else:
            nom1 = simpledialog.askstring("Nom", "Nom Joueur 1 :") or "J1"
            nom2 = simpledialog.askstring("Nom", "Nom Joueur 2 :") or "J2"
            self.joueurs = [Player(nom1), Player(nom2)]
        self.joueur_actuel = 0
        self.phase_placement()

    # ---------- placement ----------
    def phase_placement(self):
        # Affiche la phase de placement pour self.joueur_actuel
        self.clear_all()
        joueur = self.joueurs[self.joueur_actuel]

        if joueur.types_restants:
            self.bateau_a_placer = joueur.types_restants[0]

            # header
            self.header_frame = tk.Frame(self.root)
            self.header_frame.pack(pady=6)
            tk.Label(self.header_frame, text=f"{joueur.name}, placez votre {self.bateau_a_placer}").pack()
            frame_o = tk.Frame(self.header_frame)
            frame_o.pack(pady=4)
            for ori in ['N', 'E', 'S', 'W']:
                tk.Button(frame_o, text=ori, width=3, command=lambda o=ori: self.set_orientation(o)).pack(side="left", padx=2)

            # grille du joueur (afficher B pendant placement)
            self.create_plateau(joueur, placer=True)
        else:
            # ce joueur a fini ; on passe au suivant ou on commence la phase de tir
            if self.joueur_actuel == 0:
                # passer au 1 pour placer
                self.joueur_actuel = 1
                if self.joueurs[self.joueur_actuel].is_ia:
                    # IA place tout
                    for t in list(self.joueurs[self.joueur_actuel].types_restants):
                        self.joueurs[self.joueur_actuel].placer_bateau_aleatoire(t)
                    self.joueurs[self.joueur_actuel].types_restants.clear()
                    # revenir au joueur 0 et commencer tir
                    self.joueur_actuel = 0
                    self.phase_tir()
                else:
                    self.phase_placement()
            else:
                # si on était joueur 1, revenir à 0 et commencer tir
                self.joueur_actuel = 0
                self.phase_tir()

    def set_orientation(self, ori):
        self.orientation = ori

    def placer_bateau_click(self, row, col):
        joueur = self.joueurs[self.joueur_actuel]
        type_bat = self.bateau_a_placer
        bateau = Bateau(type_bat)
        try:
            joueur._placer_bateau_logique(bateau, row, col, self.orientation)
        except:
            # placement invalide : on ignore (on peut afficher message si tu veux)
            return
        # retirer le type posé si présent
        if type_bat in joueur.types_restants:
            joueur.types_restants.remove(type_bat)
        # réafficher la phase placement (soit prochain bateau, soit joueur suivant)
        self.phase_placement()

    # ---------- affichage plateau ----------
    def create_plateau(self, joueur, placer=False):
        # détruit ancienne grid si existante
        if self.grid_frame:
            self.grid_frame.destroy()
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack(padx=6, pady=6)
        self.buttons = []

        for r in range(TAILLE):
            row_btns = []
            for c in range(TAILLE):
                val = joueur.plateau[r][c]
                attaquable = joueur.cases_attaquable[r][c]

                # Si on est en placement (on affiche les B visibles pour le joueur)
                if placer:
                    if val == "B":
                        text, couleur = "B", "green"
                    elif not attaquable:
                        text, couleur = "O", "lightblue"
                    elif val == "X":
                        text, couleur = "X", "red"
                    else:
                        text, couleur = "O", "lightblue"
                else:
                    # affichage en phase de tir : on montre uniquement X (touché) et O (raté) ; jamais B
                    if val == "X":
                        text, couleur = "X", "red"
                    elif not attaquable:
                        text, couleur = "O", "lightblue"
                    else:
                        text, couleur = "O", "lightgray"

                b = tk.Button(self.grid_frame, text=text, width=2, height=1, bg=couleur)
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
        joueur = self.joueurs[self.joueur_actuel]
        adv = self.joueurs[1 - self.joueur_actuel]

        # header + info label
        self.header_frame = tk.Frame(self.root)
        self.header_frame.pack(pady=6)
        tk.Label(self.header_frame, text=f"{joueur.name}, à vous de tirer !").pack()
        self.info_tir = tk.Label(self.header_frame, text="", font=("Arial", 14))
        self.info_tir.pack()

        # afficher la grille de l'adversaire (bateaux invisibles)
        self.create_plateau(adv, placer=False)

        # si l'IA doit jouer, on déclenche après un court délai
        if joueur.is_ia:
            self.root.after(500, self.ia_tirer)

    def tirer_click(self, row, col):
        joueur = self.joueurs[self.joueur_actuel]
        adv = self.joueurs[1 - self.joueur_actuel]

        # si déjà ciblée -> ignore
        if not adv.cases_attaquable[row][col]:
            return

        # marquer ciblée
        adv.cases_attaquable[row][col] = False
        val = adv.plateau[row][col]

        if val == "B":
            # touché
            adv.plateau[row][col] = "X"
            # mettre à jour bouton affiché (on affiche la grille de l'adversaire)
            try:
                self.buttons[row][col].config(text="X", bg="red")
            except:
                pass
            if self.info_tir:
                self.info_tir.config(text="🎯 Touché !", fg="red")
            # vérifier victoire
            if adv.tous_coules():
                self.clear_header_and_grid()
                self.header_frame = tk.Frame(self.root)
                self.header_frame.pack(pady=10)
                tk.Label(self.header_frame, text=f"{joueur.name} a gagné !", font=("Arial", 16)).pack()
                return
            # joueur touche -> il rejoue ; réaffiche (petit délai pour voir la case)
            self.root.update()
            self.root.after(300, self.phase_tir)
        else:
            # raté
            adv.plateau[row][col] = "O"
            try:
                self.buttons[row][col].config(text="O", bg="lightblue")
            except:
                pass
            if self.info_tir:
                self.info_tir.config(text="💧 Dans l'eau !", fg="blue")
            # passe au joueur suivant
            self.joueur_actuel = 1 - self.joueur_actuel
            self.root.update()
            # on attend un court délai puis on montre la grille du joueur suivant
            self.root.after(300, self.phase_tir)

    # ---------- IA ----------
    def ia_tirer(self):
        if not self.joueurs[self.joueur_actuel].is_ia:
            return
        adv = self.joueurs[1 - self.joueur_actuel]
        options = [(r, c) for r in range(TAILLE) for c in range(TAILLE) if adv.cases_attaquable[r][c]]
        if not options:
            return
        row, col = random.choice(options)
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
