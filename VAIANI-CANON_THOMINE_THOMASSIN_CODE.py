import copy
import random

class TicTacToe:
    def __init__(self):
        self.grille = [[" "]*3 for _ in range(3)]
        
    def coup(self, ligne, colonne, symbole):
        if self.grille[ligne][colonne] == " ":
            self.grille[ligne][colonne] = symbole
            return True
        return False

    def victoire(self, symbole):
        for ligne in self.grille:
            if all(s == symbole for s in ligne):
                return True
        for colonne in range(3):
            if all(ligne[colonne] == symbole for ligne in self.grille):
                return True
        if self.grille[0][0] == self.grille[1][1] == self.grille[2][2] == symbole:
            return True
        if self.grille[0][2] == self.grille[1][1] == self.grille[2][0] == symbole:
            return True
        return False

    def plein(self):
        for ligne in self.grille:
            if any(s == " " for s in ligne):
                return False
        return True


class UltimateTicTacToe:
    def __init__(self):
        self.grilles = [[TicTacToe() for _ in range(3)] for _ in range(3)]
        self.symbole_actuel = "X"
        self.grille_actuelle = None
        self.compteur_coups = 0
        self.gagnant = [[" "]*3 for _ in range(3)]

    def coup(self, grille_ligne, grille_colonne, ligne, colonne):
        if self.compteur_coups > 0 and (self.grille_actuelle is not None and (grille_ligne, grille_colonne) != self.grille_actuelle):
            return False
        if self.gagnant[grille_ligne][grille_colonne] != " " or self.grilles[grille_ligne][grille_colonne].plein():
            return False
        if self.grilles[grille_ligne][grille_colonne].coup(ligne, colonne, self.symbole_actuel):
            if self.grilles[grille_ligne][grille_colonne].victoire(self.symbole_actuel):
                self.gagnant[grille_ligne][grille_colonne] = self.symbole_actuel
            self.grille_actuelle = (ligne, colonne) if not self.grilles[ligne][colonne].plein() and self.gagnant[ligne][colonne] == " " else None
            self.symbole_actuel = "X" if self.symbole_actuel == "O" else "O"
            self.compteur_coups += 1
            return True
        return False

    def victoire(self):
        for symbole in ("X", "O"):
            for i in range(3):
                if all(self.gagnant[i][j] == symbole for j in range(3)):
                    return symbole
                if all(self.gagnant[j][i] == symbole for j in range(3)):
                    return symbole
            if all(self.gagnant[i][i] == symbole for i in range(3)):
                return symbole
            if all(self.gagnant[i][2-i] == symbole for i in range(3)):
                return symbole
        return None

    def plein(self):
        for ligne in self.grilles:
            for grille in ligne:
                if not grille.plein():
                    return False
        return True

    def afficher(self):
        for i in range(3):
            for x in range(3):
                for j in range(3):
                    print(" ".join(self.grilles[i][j].grille[x]), end=" | ")
                print()
            print("-------------------------")
        print("Prochain joueur:", self.symbole_actuel)
        
    def actions(self):
        actions = []
        
        if self.compteur_coups > 0 and self.grille_actuelle is not None:
            grille_ligne, grille_colonne = self.grille_actuelle
            if self.gagnant[grille_ligne][grille_colonne] == " " and not self.grilles[grille_ligne][grille_colonne].plein():
                grille = self.grilles[grille_ligne][grille_colonne].grille
                for ligne in range(3):
                    for colonne in range(3):
                        if grille[ligne][colonne] == " ":
                            actions.append((grille_ligne, grille_colonne, ligne, colonne))
        else:
            for grille_ligne in range(3):
                for grille_colonne in range(3):
                    if self.gagnant[grille_ligne][grille_colonne] == " " and not self.grilles[grille_ligne][grille_colonne].plein():
                        grille = self.grilles[grille_ligne][grille_colonne].grille
                        for ligne in range(3):
                            for colonne in range(3):
                                if grille[ligne][colonne] == " ":
                                    actions.append((grille_ligne, grille_colonne, ligne, colonne))
                                
        return actions


    def result(self, action):
        grille_ligne, grille_colonne, ligne, colonne = action
        next_game = copy.deepcopy(self)
        next_game.coup(grille_ligne, grille_colonne, ligne, colonne)
        return next_game

    def terminal_test(self):
        return self.victoire() is not None or self.plein()

    def utility(self):
        victoire = self.victoire()
        if victoire is not None:
            return 100000 if victoire == "X" else -100000
        else:
            score = 0
            if self.grille_actuelle is not None:
                grilles = [self.grilles[self.grille_actuelle[0]][self.grille_actuelle[1]]]
            else:
                grilles = [grille for ligne in self.grilles for grille in ligne]
            for grille in grilles:
                for k in range(3):
                    for l in range(3):
                        symbole = grille.grille[k][l]
                        if symbole != " ":
                            # Priorité aux centres
                            valeurcentre=1
                            if self.compteur_coups==0:
                                valeurcentre= 100
                            if (k, l) == (1, 1):
                                score += valeurcentre if symbole == "X" else -valeurcentre
                            # Verifie 2 et 3 d'affilés
                            directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
                            for dx, dy in directions:
                                try:
                                    if k + dx >= 0 and l + dy >= 0 and grille.grille[k + dx][l + dy] == symbole:
                                        score += 2 if symbole == "X" else -2
                                    if k + 2*dx >= 0 and l + 2*dy >= 0 and grille.grille[k + 2*dx][l + 2*dy] == symbole:
                                        score += 20 if symbole == "X" else -20
                                except IndexError:
                                    pass
            return score


    def minimax_alphabeta(self, depth, player, alpha, beta):
        if self.terminal_test() or depth == 0:
            return None, self.utility()

        best_actions = []
        best_value = float('-inf') if player == "X" else float('inf')
    
        for action in self.actions():
            next_state = self.result(action)
            _, value = next_state.minimax_alphabeta(depth - 1, "O" if player == "X" else "X", alpha, beta)
    
            if player == "X":
                if value > best_value:
                    best_value = value
                    best_actions = [action]
                elif value == best_value:
                    best_actions.append(action)
                alpha = max(alpha, best_value)
            else:
                if value < best_value:
                    best_value = value
                    best_actions = [action]
                elif value == best_value:
                    best_actions.append(action)
                beta = min(beta, best_value)
    
            if alpha >= beta:
                break


        best_action = random.choice(best_actions)
        return best_action, best_value

    def jouer_IA(self, depth):
        action, _ = self.minimax_alphabeta(depth, self.symbole_actuel, float('-inf'), float('inf'))
        if action:
            print(action)
            self.coup(*action)    
        
    def choisir_premier_joueur(self):
        choix = input("Qui commence ? Humain (H) ou IA (I) ? ")
        if choix.lower() == "h":
            symbole_humain = "X"
            print("Le joueur humain commence et joue avec le symbole 'X'.")
            return symbole_humain
        elif choix.lower() == "i":
            symbole_humain = "O"
            print("L'IA commence et joue avec le symbole 'X'.")
            return symbole_humain
        else:
            print("Choix invalide. Veuillez réessayer.")
            return self.choisir_premier_joueur()
        


def jouer():
    jeu = UltimateTicTacToe()
    symbole_humain = jeu.choisir_premier_joueur()
    while not jeu.victoire() and not jeu.plein():
        jeu.afficher()
        if jeu.symbole_actuel == symbole_humain:
            if jeu.compteur_coups == 0 or jeu.grille_actuelle is None:
                entrée=[]
                while len(entrée)!= 4:
                    print("Entrer la grille (ligne colonne) et le coup (ligne colonne): \nEXEMPLE: 0 0 0 0 joue dans la grille en haut à gauche dans la case en haut à gauche")
                    entrée = input().split()
                if jeu.coup(int(entrée[0]), int(entrée[1]), int(entrée[2]), int(entrée[3])):
                    continue
            else:
                print("Entrer le coup (ligne colonne) dans la grille", jeu.grille_actuelle, ":\nEXEMPLE: 0 0 joue dans la grille en haut à gauche")
                entrée = input().split()
                if jeu.coup(jeu.grille_actuelle[0], jeu.grille_actuelle[1], int(entrée[0]), int(entrée[1])):
                    continue
            print("Coup non valide. Réessayez.")
        else:
            jeu.jouer_IA(5)
    jeu.afficher()
    if jeu.victoire():
        print("Le joueur", jeu.victoire(), "a gagné.")
    else:
        print("Match nul.")

jouer()
