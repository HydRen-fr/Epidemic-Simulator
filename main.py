# Importation des modules nécessaires.
import pygame  # Bibliothèque pour la création de jeux vidéo.
import random  # Module pour la génération de nombres aléatoires.
import sys  # Module fournissant un accès à certaines variables utilisées ou maintenues par l'interpréteur Python.

# Constantes définissant les paramètres du programme.
LARGEUR_ECRAN = 800  # Largeur de la fenêtre de la simulation.
HAUTEUR_ECRAN = 600  # Hauteur de la fenêtre de la simulation.
COULEUR_MUR = (0, 0, 0)  # Couleur des murs (en noir).
COULEUR_FOND = (255, 255, 255)  # Couleur du fond de la fenêtre (en blanc).
TAILLE_CARRE = 450  # Taille du cadre où les individus évoluent.
TAILLE_INDIVIDU = 4  # Taille des individus représentés par des points.
NB_INDIVIDUS = 70  # Nombre total d'individus dans la simulation.
VITESSE_MAX = 0.4  # Vitesse maximale des individus.

# Initialisation des modules Pygame manuellement.
pygame.display.init()
pygame.font.init()

# Création de la fenêtre de simulation.
ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
pygame.display.set_caption("Simulation d'épidémie")

# Définition de la classe représentant un individu dans la simulation.
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
        # Vérifier si l'individu atteint les bords du cadre et les fait rebondir en conséquence.
        if self.x - self.taille < (LARGEUR_ECRAN - TAILLE_CARRE) // 2 or self.x + self.taille > (LARGEUR_ECRAN + TAILLE_CARRE) // 2:
            self.vitesse_x = -self.vitesse_x
        if self.y - self.taille < (HAUTEUR_ECRAN - TAILLE_CARRE) // 2 or self.y + self.taille > (HAUTEUR_ECRAN + TAILLE_CARRE) // 2:
            self.vitesse_y = -self.vitesse_y

    def detecter_collision(self, autre_individu):
        # Calculer la distance entre deux individus et tester s'ils entrent en collision.
        distance = ((self.x - autre_individu.x) ** 2 + (self.y - autre_individu.y) ** 2) ** 0.5
        return distance <= self.taille + autre_individu.taille

# Création d'une liste d'individus pour la simulation.
individus = [Individu(
    random.randint((LARGEUR_ECRAN - TAILLE_CARRE) // 2 + TAILLE_INDIVIDU, (LARGEUR_ECRAN + TAILLE_CARRE) // 2 - TAILLE_INDIVIDU),
    random.randint((HAUTEUR_ECRAN - TAILLE_CARRE) // 2 + TAILLE_INDIVIDU, (HAUTEUR_ECRAN + TAILLE_CARRE) // 2 - TAILLE_INDIVIDU),
    TAILLE_INDIVIDU,
    (255, 0, 0)  # Couleur rouge pour le premier individu.
) for _ in range(1)] + [Individu(
    random.randint((LARGEUR_ECRAN - TAILLE_CARRE) // 2 + TAILLE_INDIVIDU, (LARGEUR_ECRAN + TAILLE_CARRE) // 2 - TAILLE_INDIVIDU),
    random.randint((HAUTEUR_ECRAN - TAILLE_CARRE) // 2 + TAILLE_INDIVIDU, (HAUTEUR_ECRAN + TAILLE_CARRE) // 2 - TAILLE_INDIVIDU),
    TAILLE_INDIVIDU,
    (0, 0, 255)  # Couleur bleu pour les autres individus.
) for _ in range(NB_INDIVIDUS - 1)]

# Boucle principale de la simulation.
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Dessiner le fond blanc.
    ecran.fill(COULEUR_FOND)

    # Dessiner le cadre noir.
    pygame.draw.rect(ecran, COULEUR_MUR, pygame.Rect((LARGEUR_ECRAN - TAILLE_CARRE) // 2, (HAUTEUR_ECRAN - TAILLE_CARRE) // 2, TAILLE_CARRE, TAILLE_CARRE), 2)

    # Déplacer et faire rebondir les individus dans le cadre.
    for individu in individus:
        individu.bouger()
        individu.rebondir_sur_murs()
        individu.dessiner()

    # Tester les collisions entre les individus et mettre à jour les couleurs en cas de collision.
    for i in range(len(individus)):
        for j in range(len(individus)):
            if i != j and individus[i].detecter_collision(individus[j]):
                individus[i].couleur, individus[j].couleur = (255, 0, 0), (255, 0, 0)  # Les individus en collision deviennent rouges.

    # Mettre à jour l'affichage de la simulation.
    pygame.display.flip()
