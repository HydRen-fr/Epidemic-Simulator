import pygame
import random
import sys

# Constantes
LARGEUR_ECRAN = 800
HAUTEUR_ECRAN = 600
COULEUR_MUR = (0, 0, 0)  # Noir
COULEUR_FOND = (255, 255, 255)  # Blanc
TAILLE_CARRE = 450
TAILLE_INDIVIDU = 4
NB_INDIVIDUS = 70
VITESSE_MAX = 0.4

# Initialisation des modules Pygame manuellement
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
        self.vitesse_x = random.uniform(-VITESSE_MAX, VITESSE_MAX)
        self.vitesse_y = random.uniform(-VITESSE_MAX, VITESSE_MAX)

    def dessiner(self):
        pygame.draw.circle(ecran, self.couleur, (int(self.x), int(self.y)), self.taille)

    def bouger(self):
        self.x += self.vitesse_x
        self.y += self.vitesse_y

    def rebondir_sur_murs(self):
        if self.x - self.taille < (LARGEUR_ECRAN - TAILLE_CARRE) // 2 or self.x + self.taille > (LARGEUR_ECRAN + TAILLE_CARRE) // 2:
            self.vitesse_x = -self.vitesse_x
        if self.y - self.taille < (HAUTEUR_ECRAN - TAILLE_CARRE) // 2 or self.y + self.taille > (HAUTEUR_ECRAN + TAILLE_CARRE) // 2:
            self.vitesse_y = -self.vitesse_y

    def detecter_collision(self, autre_individu):
        distance = ((self.x - autre_individu.x) ** 2 + (self.y - autre_individu.y) ** 2) ** 0.5
        return distance <= self.taille + autre_individu.taille

# Création d'une liste d'Individus
individus = [Individu(
    random.randint((LARGEUR_ECRAN - TAILLE_CARRE) // 2 + TAILLE_INDIVIDU, (LARGEUR_ECRAN + TAILLE_CARRE) // 2 - TAILLE_INDIVIDU),
    random.randint((HAUTEUR_ECRAN - TAILLE_CARRE) // 2 + TAILLE_INDIVIDU, (HAUTEUR_ECRAN + TAILLE_CARRE) // 2 - TAILLE_INDIVIDU),
    TAILLE_INDIVIDU,
    (255, 0, 0)  # Rouge pour le premier individu
) for _ in range(1)] + [Individu(
    random.randint((LARGEUR_ECRAN - TAILLE_CARRE) // 2 + TAILLE_INDIVIDU, (LARGEUR_ECRAN + TAILLE_CARRE) // 2 - TAILLE_INDIVIDU),
    random.randint((HAUTEUR_ECRAN - TAILLE_CARRE) // 2 + TAILLE_INDIVIDU, (HAUTEUR_ECRAN + TAILLE_CARRE) // 2 - TAILLE_INDIVIDU),
    TAILLE_INDIVIDU,
    (0, 0, 255)  # Bleu pour le deuxième individu
) for _ in range(NB_INDIVIDUS - 1)]

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

    # Déplacer et faire rebondir les Individus
    for individu in individus:
        individu.bouger()
        individu.rebondir_sur_murs()
        individu.dessiner()

    # Tester les collisions et mettre à jour les couleurs
    for i in range(len(individus)):
        for j in range(len(individus)):
            if i != j and individus[i].detecter_collision(individus[j]):
                individus[i].couleur, individus[j].couleur = (255, 0, 0), (255, 0, 0)  # Rouges tous les deux

    # Mettre à jour l'affichage
    pygame.display.flip()
