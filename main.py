import pygame
import sys

# Constantes pour la taille du plateau et des cases
TAILLE_CASE = 80
NOMBRE_CASES = 10

# Constantes pour les couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
BLEU = (0, 0, 255)
VERT = (0, 255, 0)

# Initialisation de Pygame
pygame.init()

# Création de la fenêtre
fenetre = pygame.display.set_mode((TAILLE_CASE * NOMBRE_CASES, TAILLE_CASE * NOMBRE_CASES))

# Fonction pour dessiner le plateau
def dessiner_plateau():
    fenetre.fill(NOIR)
    for i in range(NOMBRE_CASES):
        for j in range(NOMBRE_CASES):
            if (i + j) % 2 == 0:
                pygame.draw.rect(fenetre, BLANC, (i * TAILLE_CASE, j * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE))

# Fonction pour dessiner les pions
def dessiner_pions(pions):
    for pion in pions:
        pygame.draw.circle(fenetre, ROUGE if pion[2] == 1 else BLEU, (pion[0] * TAILLE_CASE + TAILLE_CASE // 2, pion[1] * TAILLE_CASE + TAILLE_CASE // 2), TAILLE_CASE // 2 - 10)

# Initialisation des pions
pions = [(i, j, 1) for i in range(NOMBRE_CASES) for j in range(4) if (i + j) % 2 == 0] + [(i, j, 2) for i in range(NOMBRE_CASES) for j in range(6, NOMBRE_CASES) if (i + j) % 2 == 0]

# Ajout d'une variable pour le pion sélectionné
pion_selectionne = None

# Ajout d'une variable pour le tour
tour = 1

# Fonction pour gérer les clics de la souris
def gerer_clic(x, y):
    global pion_selectionne
    if pion_selectionne is None:
        for pion in pions:
            if pion[0] == x and pion[1] == y and pion[2] == tour:
                pion_selectionne = pion
    else:
        if est_mouvement_valide(pion_selectionne, x, y):
            pions.remove(pion_selectionne)
            pions.append((x, y, pion_selectionne[2]))
            pion_selectionne = None


# Fonction pour vérifier si un mouvement est valide
def est_mouvement_valide(pion, x, y):
    global pions, tour
    dx = x - pion[0]
    dy = y - pion[1]
    if abs(dx) != abs(dy):
        return False
    if pion[2] == 1 and dy < 0:
        return False
    if pion[2] == 2 and dy > 0:
        return False
    if abs(dx) == 2:
        pion_pris = (pion[0] + dx // 2, pion[1] + dy // 2)
        for p in pions:
            if p[0] == pion_pris[0] and p[1] == pion_pris[1] and p[2] != pion[2]:
                pions.remove(p)
                tour = 3 - tour
                return True
    tour = 3 - tour
    return True


# Fonction pour calculer les déplacements possibles d'un pion
def calculer_deplacements_possibles(pion):
    deplacements = []
    for dx in [-1, 1]:
        dy = 1 if pion[2] == 1 else -1  # Les pions rouges (1) se déplacent vers le bas (1), les pions noirs (2) se déplacent vers le haut (-1)
        x = pion[0] + dx
        y = pion[1] + dy
        if 0 <= x < NOMBRE_CASES and 0 <= y < NOMBRE_CASES:
            if (x, y, 3 - pion[2]) in pions:
                continue
            if (x, y, pion[2]) in pions:
                continue
            deplacements.append((x, y))
    return deplacements

# Fonction pour dessiner les déplacements possibles
def dessiner_deplacements_possibles(deplacements):
    for x, y in deplacements:
        pygame.draw.circle(fenetre, VERT, (x * TAILLE_CASE + TAILLE_CASE // 2, y * TAILLE_CASE + TAILLE_CASE // 2), TAILLE_CASE // 2 - 10)

# Boucle principale du jeu
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            x = x // TAILLE_CASE
            y = y // TAILLE_CASE
            gerer_clic(x, y)

    dessiner_plateau()
    dessiner_pions(pions)
    if pion_selectionne is not None:
        dessiner_deplacements_possibles(calculer_deplacements_possibles(pion_selectionne))

    pygame.display.flip()