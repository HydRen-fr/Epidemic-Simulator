import pygame
import random
import sys

# Constantes
LARGEUR_ECRAN = 800
HAUTEUR_ECRAN = 600
COULEUR_MUR = (0, 0, 0)  # Noir
COULEUR_FOND = (255, 255, 255)  # Blanc
TAILLE_CARRE = 230
TAILLE_INDIVIDU = 5
NB_INDIVIDUS = 50

# Initialisation des modules pygame manuellement
# pygame.init() fait tout d'un coup et peut créer des bugs
pygame.display.init()
pygame.font.init()

# Création de la fenêtre
ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
pygame.display.set_caption("Simulation d'épidémie")

class Individu:
    def __init__(self, x, y, taille, couleur):
        self.x = x
        self.y = y
        self.taille = taille
        self.couleur = couleur

    def dessiner(self):
        pygame.draw.circle(ecran, self.couleur, (int(self.x), int(self.y)), self.taille)

# Création d'une liste d'Individus
individus = [Individu(
    random.randint((LARGEUR_ECRAN - TAILLE_CARRE) // 2, (LARGEUR_ECRAN + TAILLE_CARRE) // 2),
    random.randint((HAUTEUR_ECRAN - TAILLE_CARRE) // 2, (HAUTEUR_ECRAN + TAILLE_CARRE) // 2),
    TAILLE_INDIVIDU,
    (0, 120, 240)
) for _ in range(NB_INDIVIDUS)]

# Boucle principale
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Dessiner le fond blanc
    ecran.fill(COULEUR_FOND)

    # Dessiner le carré noir
    pygame.draw.rect(ecran, COULEUR_MUR, pygame.Rect((LARGEUR_ECRAN - TAILLE_CARRE) // 2, (HAUTEUR_ECRAN - TAILLE_CARRE) // 2, TAILLE_CARRE, TAILLE_CARRE), 2)

    # Dessiner les Individus
    for ind in individus:
        ind.dessiner()

    # Mettre à jour l'affichage
    pygame.display.flip()

